from __future__ import annotations

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.schemas.backtest import BacktestCreateRequest
from app.services.technical_analysis_service import TechnicalAnalysisService
from app.technical_analysis import get_strategy
from app.technical_analysis.backtester import run_backtest
from app.technical_analysis.strategies import StrategyParameterError


class BacktestService:
    def __init__(self, technical_analysis_service: TechnicalAnalysisService):
        self.technical_analysis_service = technical_analysis_service

    def create_backtest(self, request: BacktestCreateRequest) -> dict:
        try:
            strategy = get_strategy(request.strategy)
            requested_start, requested_end, prices = (
                self.technical_analysis_service.load_prices(
                    request.symbol,
                    request.start_date,
                    request.end_date,
                    strategy.required_history(request.parameters),
                )
            )
            signals, parameters = strategy.apply(prices, request.parameters)
            signals = signals.loc[
                (signals.index.date >= requested_start)
                & (signals.index.date <= requested_end)
            ]
            if signals.empty or not strategy.has_ready_indicators(signals):
                raise ValueError("기술 지표를 계산하기 위한 데이터가 부족합니다.")
            metrics = run_backtest(
                signals,
                request.initial_capital,
                request.commission_rate,
                request.slippage_rate,
            )
        except (StrategyParameterError, ValueError) as exc:
            raise ProjectException(ErrorCode.BACKTEST400_1) from exc

        return {
            "symbol": request.symbol.upper(),
            "strategy": strategy.name.value,
            "strategy_display_name": strategy.display_name,
            "parameters": parameters,
            "period": {
                "start_date": requested_start.isoformat(),
                "end_date": requested_end.isoformat(),
            },
            "execution_policy": {
                "position": "long_only_all_in",
                "signal_price": "close",
                "execution_price": "next_session_open",
                "commission_rate": request.commission_rate,
                "slippage_rate": request.slippage_rate,
            },
            **metrics,
            "disclaimer": "과거 성과는 미래 수익을 보장하지 않습니다.",
        }
