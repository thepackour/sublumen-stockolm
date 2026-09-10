from __future__ import annotations

from datetime import date, datetime, timedelta
from numbers import Real

import pandas as pd

from app.clients.fdr_client import FdrClient
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.technical_analysis import StrategyName, get_strategy, list_strategies
from app.technical_analysis.strategies import StrategyParameterError


class TechnicalAnalysisService:
    DEFAULT_LOOKBACK_DAYS = 365
    WARMUP_CALENDAR_DAYS = 180

    def __init__(self, fdr_client: FdrClient):
        self.fdr_client = fdr_client

    @staticmethod
    def available_strategies() -> list[dict]:
        return list_strategies()

    def analyze(
        self,
        symbol: str,
        strategy_name: StrategyName | str,
        start_date: date | None = None,
        end_date: date | None = None,
        parameters: dict[str, float] | None = None,
        include_history: bool = True,
    ) -> dict:
        try:
            strategy = get_strategy(strategy_name)
        except StrategyParameterError as exc:
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_1) from exc
        try:
            required_history = strategy.required_history(parameters)
            requested_start, requested_end, prices = self.load_prices(
                symbol,
                start_date,
                end_date,
                required_history,
            )
            analyzed, resolved_parameters = strategy.apply(prices, parameters)
        except StrategyParameterError as exc:
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_1) from exc

        analyzed = analyzed.loc[
            (analyzed.index.date >= requested_start)
            & (analyzed.index.date <= requested_end)
        ]
        if len(analyzed) < 2 or analyzed["close"].isna().all():
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_2)

        if not strategy.has_ready_indicators(analyzed):
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_2)

        latest = analyzed.iloc[-1]
        result = {
            "symbol": symbol.upper(),
            "strategy": strategy.name.value,
            "strategy_display_name": strategy.display_name,
            "parameters": resolved_parameters,
            "period": {
                "start_date": requested_start.isoformat(),
                "end_date": requested_end.isoformat(),
            },
            "latest": self._record(analyzed.index[-1], latest),
            "disclaimer": "기술적 지표는 투자 판단을 돕는 참고자료이며 수익을 보장하지 않습니다.",
        }
        if include_history:
            result["history"] = [
                self._record(index, row)
                for index, row in analyzed.iterrows()
            ]
        return result

    def load_prices(
        self,
        symbol: str,
        start_date: date | str | None,
        end_date: date | str | None,
        warmup_periods: int = 0,
    ) -> tuple[date, date, pd.DataFrame]:
        today = datetime.now().date()
        start_date = self._coerce_date(start_date)
        end_date = self._coerce_date(end_date)
        requested_end = end_date or today
        requested_start = start_date or (
            requested_end - timedelta(days=self.DEFAULT_LOOKBACK_DAYS)
        )
        if requested_start > requested_end:
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_1)

        warmup_days = max(self.WARMUP_CALENDAR_DAYS, warmup_periods * 2)
        fetch_start = requested_start - timedelta(days=warmup_days)
        try:
            raw = self.fdr_client.get_stock_price(
                symbol,
                fetch_start.isoformat(),
                requested_end.isoformat(),
            )
        except Exception as exc:
            raise ProjectException(ErrorCode.STOCK404_1) from exc

        prices = self._normalize_prices(raw)
        if prices.empty:
            raise ProjectException(ErrorCode.STOCK404_1)
        return requested_start, requested_end, prices

    @staticmethod
    def _coerce_date(value: date | str | None) -> date | None:
        if value is None or isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_1) from exc

    @staticmethod
    def _normalize_prices(raw: pd.DataFrame) -> pd.DataFrame:
        prices = raw.rename(columns=lambda value: str(value).strip().lower()).copy()
        if not {"open", "close"}.issubset(prices.columns):
            raise ProjectException(ErrorCode.TECHNICAL_ANALYSIS400_2)
        prices.index = pd.to_datetime(prices.index)
        prices = prices[~prices.index.duplicated(keep="last")].sort_index()
        return prices.dropna(subset=["open", "close"])

    @staticmethod
    def _record(index, row: pd.Series) -> dict:
        record = {
            "date": index.date().isoformat() if hasattr(index, "date") else str(index),
        }
        for column, value in row.items():
            if pd.isna(value):
                record[column] = None
            elif isinstance(value, Real):
                record[column] = round(float(value), 4)
            else:
                record[column] = value
        return record
