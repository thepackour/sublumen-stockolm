from __future__ import annotations

from langchain_core.tools import StructuredTool

from app.schemas.backtest import BacktestCreateRequest
from app.services.backtest_service import BacktestService
from app.services.stock_search_service import StockSearchService


class BacktestTool:
    """Tools owned by the future Portfolio or Risk Management Agent."""

    def __init__(
        self,
        service: BacktestService,
        stock_search_service: StockSearchService,
    ):
        self.service = service
        self.stock_search_service = stock_search_service

    def backtest_technical_strategy(
        self,
        stock: str,
        strategy: str = "sma_crossover",
        start_date: str | None = None,
        end_date: str | None = None,
        initial_capital: float = 1_000_000.0,
        parameters: dict[str, float] | None = None,
    ) -> dict:
        """종목과 기술적 전략의 과거 성과를 검증한다."""
        print("backtest_technical_strategy is used.")

        symbol = self.stock_search_service.find_symbol(stock)
        request = BacktestCreateRequest(
            symbol=symbol,
            strategy=strategy,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            parameters=parameters or {},
        )
        result = self.service.create_backtest(request)
        result.pop("equity_curve", None)
        return result

    def get_tools(self) -> list[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.backtest_technical_strategy,
                name="backtest_technical_strategy",
                description=(
                    "기술적 전략의 수익률, 단순보유 대비 성과, 최대 낙폭, 샤프 지수, "
                    "거래 횟수와 승률을 검증한다."
                ),
            )
        ]
