from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from math import isfinite
from numbers import Real

import pandas as pd

from app.technical_analysis.indicators import (
    bollinger_bands,
    relative_strength_index,
    simple_moving_average,
)


class StrategyName(str, Enum):
    SMA_CROSSOVER = "sma_crossover"
    RSI_REBOUND = "rsi_rebound"
    BOLLINGER_REBOUND = "bollinger_rebound"


class StrategyParameterError(ValueError):
    pass


class TechnicalStrategy(ABC):
    name: StrategyName
    display_name: str
    description: str
    default_parameters: dict[str, float]
    indicator_columns: tuple[str, ...]

    def resolve_parameters(self, supplied: dict[str, float] | None) -> dict[str, float]:
        supplied = supplied or {}
        unknown = supplied.keys() - self.default_parameters.keys()
        if unknown:
            raise StrategyParameterError(
                f"지원하지 않는 파라미터입니다: {', '.join(sorted(unknown))}"
            )
        if any(
            not isinstance(value, Real)
            or isinstance(value, bool)
            or not isfinite(float(value))
            for value in supplied.values()
        ):
            raise StrategyParameterError("전략 파라미터는 숫자여야 합니다.")
        return {**self.default_parameters, **supplied}

    @staticmethod
    def _integer_parameter(parameters: dict[str, float], name: str) -> int:
        value = parameters[name]
        if int(value) != value:
            raise StrategyParameterError(f"{name}은 정수여야 합니다.")
        return int(value)

    @abstractmethod
    def apply(
        self,
        prices: pd.DataFrame,
        parameters: dict[str, float] | None = None,
    ) -> tuple[pd.DataFrame, dict[str, float]]:
        pass

    @abstractmethod
    def required_history(self, parameters: dict[str, float] | None = None) -> int:
        pass

    def metadata(self) -> dict:
        return {
            "name": self.name.value,
            "display_name": self.display_name,
            "description": self.description,
            "default_parameters": self.default_parameters,
        }

    def has_ready_indicators(self, frame: pd.DataFrame) -> bool:
        return not frame[list(self.indicator_columns)].dropna(how="any").empty

    @staticmethod
    def _signal_frame(prices: pd.DataFrame) -> pd.DataFrame:
        result = prices.copy()
        result["signal"] = "HOLD"
        result["reason"] = "조건이 충족되지 않았습니다."
        return result


class SmaCrossoverStrategy(TechnicalStrategy):
    name = StrategyName.SMA_CROSSOVER
    display_name = "이동평균 교차"
    description = "단기 이동평균선이 장기 이동평균선을 교차할 때 추세 전환을 판단합니다."
    default_parameters = {"short_window": 20, "long_window": 60}
    indicator_columns = ("sma_short", "sma_long")

    def required_history(self, parameters=None) -> int:
        resolved = self.resolve_parameters(parameters)
        return self._integer_parameter(resolved, "long_window") + 1

    def apply(self, prices, parameters=None):
        resolved = self.resolve_parameters(parameters)
        short_window = self._integer_parameter(resolved, "short_window")
        long_window = self._integer_parameter(resolved, "long_window")
        if short_window < 2 or long_window <= short_window or long_window > 500:
            raise StrategyParameterError(
                "이동평균 기간은 2 <= short_window < long_window <= 500이어야 합니다."
            )

        result = self._signal_frame(prices)
        result["sma_short"] = simple_moving_average(result["close"], short_window)
        result["sma_long"] = simple_moving_average(result["close"], long_window)
        cross_up = (
            (result["sma_short"] > result["sma_long"])
            & (result["sma_short"].shift(1) <= result["sma_long"].shift(1))
        )
        cross_down = (
            (result["sma_short"] < result["sma_long"])
            & (result["sma_short"].shift(1) >= result["sma_long"].shift(1))
        )
        result.loc[cross_up, ["signal", "reason"]] = [
            "BUY",
            "단기 이동평균선이 장기 이동평균선을 상향 돌파했습니다.",
        ]
        result.loc[cross_down, ["signal", "reason"]] = [
            "SELL",
            "단기 이동평균선이 장기 이동평균선을 하향 돌파했습니다.",
        ]
        return result, resolved


class RsiReboundStrategy(TechnicalStrategy):
    name = StrategyName.RSI_REBOUND
    display_name = "RSI 과매도 반등"
    description = "RSI가 과매도·과매수 구간에서 기준선 안으로 돌아오는 순간을 포착합니다."
    default_parameters = {"period": 14, "oversold": 30, "overbought": 70}
    indicator_columns = ("rsi",)

    def required_history(self, parameters=None) -> int:
        resolved = self.resolve_parameters(parameters)
        return self._integer_parameter(resolved, "period") + 2

    def apply(self, prices, parameters=None):
        resolved = self.resolve_parameters(parameters)
        period = self._integer_parameter(resolved, "period")
        oversold = float(resolved["oversold"])
        overbought = float(resolved["overbought"])
        if period < 2 or period > 100 or not 0 < oversold < overbought < 100:
            raise StrategyParameterError(
                "RSI는 2 <= period <= 100, 0 < oversold < overbought < 100이어야 합니다."
            )

        result = self._signal_frame(prices)
        result["rsi"] = relative_strength_index(result["close"], period)
        rebound = (result["rsi"] >= oversold) & (result["rsi"].shift(1) < oversold)
        retreat = (result["rsi"] <= overbought) & (result["rsi"].shift(1) > overbought)
        result.loc[rebound, ["signal", "reason"]] = [
            "BUY",
            "RSI가 과매도 구간에서 반등했습니다.",
        ]
        result.loc[retreat, ["signal", "reason"]] = [
            "SELL",
            "RSI가 과매수 구간에서 내려왔습니다.",
        ]
        return result, resolved


class BollingerReboundStrategy(TechnicalStrategy):
    name = StrategyName.BOLLINGER_REBOUND
    display_name = "볼린저 밴드 반등"
    description = "가격이 하단 밴드 밖에서 복귀하면 매수하고 중심선 도달 시 매도합니다."
    default_parameters = {"window": 20, "standard_deviations": 2.0}
    indicator_columns = (
        "bollinger_middle",
        "bollinger_upper",
        "bollinger_lower",
    )

    def required_history(self, parameters=None) -> int:
        resolved = self.resolve_parameters(parameters)
        return self._integer_parameter(resolved, "window") + 1

    def apply(self, prices, parameters=None):
        resolved = self.resolve_parameters(parameters)
        window = self._integer_parameter(resolved, "window")
        standard_deviations = float(resolved["standard_deviations"])
        if window < 2 or window > 500 or not 0 < standard_deviations <= 5:
            raise StrategyParameterError(
                "볼린저 밴드는 2 <= window <= 500, 0 < standard_deviations <= 5여야 합니다."
            )

        result = self._signal_frame(prices)
        middle, upper, lower = bollinger_bands(
            result["close"],
            window,
            standard_deviations,
        )
        result["bollinger_middle"] = middle
        result["bollinger_upper"] = upper
        result["bollinger_lower"] = lower
        returned_inside = (
            (result["close"] >= result["bollinger_lower"])
            & (result["close"].shift(1) < result["bollinger_lower"].shift(1))
        )
        reached_middle = (
            (result["close"] >= result["bollinger_middle"])
            & (result["close"].shift(1) < result["bollinger_middle"].shift(1))
        )
        result.loc[returned_inside, ["signal", "reason"]] = [
            "BUY",
            "가격이 볼린저 하단 밴드 안으로 복귀했습니다.",
        ]
        result.loc[reached_middle, ["signal", "reason"]] = [
            "SELL",
            "가격이 볼린저 중심선에 도달했습니다.",
        ]
        return result, resolved


_STRATEGIES: dict[StrategyName, TechnicalStrategy] = {
    strategy.name: strategy
    for strategy in (
        SmaCrossoverStrategy(),
        RsiReboundStrategy(),
        BollingerReboundStrategy(),
    )
}


def get_strategy(name: StrategyName | str) -> TechnicalStrategy:
    try:
        return _STRATEGIES[StrategyName(name)]
    except (KeyError, ValueError) as exc:
        raise StrategyParameterError(f"지원하지 않는 전략입니다: {name}") from exc


def list_strategies() -> list[dict]:
    return [strategy.metadata() for strategy in _STRATEGIES.values()]
