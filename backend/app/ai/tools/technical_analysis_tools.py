from __future__ import annotations

from langchain_core.tools import StructuredTool

from app.services.technical_analysis_service import TechnicalAnalysisService
from app.services.stock_search_service import StockSearchService


class TechnicalAnalysisTool:
    """Tools owned by the future Technical Analysis Agent."""

    def __init__(
        self,
        service: TechnicalAnalysisService,
        stock_search_service: StockSearchService,
    ):
        self.service = service
        self.stock_search_service = stock_search_service

    def analyze_technical_indicators(
        self,
        stock: str,
        strategy: str = "sma_crossover",
        start_date: str | None = None,
        end_date: str | None = None,
        parameters: dict[str, float] | None = None,
    ) -> dict:
        """종목의 기술 지표와 최신 매매 신호를 계산한다."""
        symbol = self.stock_search_service.find_symbol(stock)
        result = self.service.analyze(
            symbol=symbol,
            strategy_name=strategy,
            start_date=start_date,
            end_date=end_date,
            parameters=parameters,
            include_history=False,
        )
        return result

    def get_tools(self) -> list[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.analyze_technical_indicators,
                name="analyze_technical_indicators",
                description=(
                    "종목명 또는 종목 코드와 전략을 받아 기술 지표와 최신 BUY/SELL/HOLD 신호를 계산한다. "
                    "전략은 sma_crossover, rsi_rebound, bollinger_rebound 중 하나이다."
                ),
            )
        ]
