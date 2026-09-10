from datetime import date

import pandas as pd
import pytest

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.schemas.backtest import BacktestCreateRequest
from app.services.backtest_service import BacktestService
from app.services.technical_analysis_service import TechnicalAnalysisService
from app.technical_analysis.backtester import run_backtest
from app.technical_analysis.strategies import StrategyParameterError, get_strategy


def price_frame(values: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {"open": values, "close": values},
        index=pd.date_range("2026-01-01", periods=len(values)),
    )


def test_sma_strategy_emits_signals_only_on_crossovers():
    strategy = get_strategy("sma_crossover")
    result, parameters = strategy.apply(
        price_frame([10, 10, 10, 8, 6, 8, 10]),
        {"short_window": 2, "long_window": 3},
    )

    assert parameters == {"short_window": 2, "long_window": 3}
    assert result["signal"].tolist() == [
        "HOLD", "HOLD", "HOLD", "SELL", "HOLD", "HOLD", "BUY"
    ]


def test_rsi_strategy_waits_for_reentry_into_normal_range():
    result, _ = get_strategy("rsi_rebound").apply(
        price_frame([10, 9, 8, 7, 8, 9, 8]),
        {"period": 2},
    )

    assert result.iloc[3]["rsi"] == 0.0
    assert result.iloc[3]["signal"] == "HOLD"
    assert result.iloc[4]["signal"] == "BUY"
    assert result.iloc[6]["signal"] == "SELL"


def test_bollinger_strategy_buys_when_price_returns_inside_lower_band():
    result, _ = get_strategy("bollinger_rebound").apply(
        price_frame([10, 10, 10, 0, 3]),
        {"window": 3, "standard_deviations": 1},
    )

    assert result.iloc[3]["close"] < result.iloc[3]["bollinger_lower"]
    assert result.iloc[3]["signal"] == "HOLD"
    assert result.iloc[4]["signal"] == "BUY"


def test_invalid_strategy_parameters_are_rejected():
    with pytest.raises(StrategyParameterError):
        get_strategy("sma_crossover").apply(
            price_frame([1, 2, 3]),
            {"short_window": 20, "long_window": 10},
        )

    with pytest.raises(StrategyParameterError):
        get_strategy("rsi_rebound").apply(
            price_frame([1, 2, 3]),
            {"period": 2.5},
        )


def test_backtest_executes_close_signal_at_next_session_open():
    signals = pd.DataFrame(
        {
            "open": [10.0, 20.0, 30.0],
            "close": [10.0, 20.0, 30.0],
            "signal": ["BUY", "SELL", "HOLD"],
        },
        index=pd.date_range("2026-01-01", periods=3),
    )

    result = run_backtest(
        signals,
        initial_capital=100.0,
        commission_rate=0,
        slippage_rate=0,
    )

    assert result["trades"][0]["signal_date"] == "2026-01-01"
    assert result["trades"][0]["execution_date"] == "2026-01-02"
    assert result["trades"][0]["price"] == 20.0
    assert result["trades"][1]["execution_date"] == "2026-01-03"
    assert result["final_value"] == 150.0
    assert result["return_rate"] == 50.0


class FakeFdrClient:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame
        self.calls = []

    def get_stock_price(self, symbol, start, end=None):
        self.calls.append((symbol, start, end))
        return self.frame.rename(columns={"open": "Open", "close": "Close"})


def test_service_returns_agent_sized_latest_result_without_history():
    client = FakeFdrClient(price_frame([10, 10, 10, 8, 6, 8, 10]))
    service = TechnicalAnalysisService(client)

    result = service.analyze(
        symbol="005930",
        strategy_name="sma_crossover",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 7),
        parameters={"short_window": 2, "long_window": 3},
        include_history=False,
    )

    assert result["latest"]["signal"] == "BUY"
    assert result["latest"]["sma_short"] == 9.0
    assert "history" not in result
    assert client.calls[0][0] == "005930"


def test_service_reports_insufficient_market_data():
    service = TechnicalAnalysisService(FakeFdrClient(price_frame([10])))

    with pytest.raises(ProjectException) as error:
        service.analyze(
            symbol="005930",
            strategy_name="sma_crossover",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1),
            parameters={"short_window": 2, "long_window": 3},
        )

    assert error.value.code == ErrorCode.TECHNICAL_ANALYSIS400_2.code


def test_backtest_service_reuses_registered_strategy_and_price_service():
    prices = price_frame([10, 10, 10, 8, 6, 8, 10, 12])
    technical_service = TechnicalAnalysisService(FakeFdrClient(prices))
    service = BacktestService(technical_service)

    result = service.create_backtest(BacktestCreateRequest(
        symbol="005930",
        strategy="sma_crossover",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 8),
        parameters={"short_window": 2, "long_window": 3},
        initial_capital=1000,
        commission_rate=0,
        slippage_rate=0,
    ))

    assert result["strategy"] == "sma_crossover"
    assert result["execution_policy"]["execution_price"] == "next_session_open"
    assert result["trades"][0]["side"] == "BUY"
    assert len(result["equity_curve"]) == 8
