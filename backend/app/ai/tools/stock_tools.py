from langchain_core.tools import StructuredTool

from app.services.stock_search_service import StockSearchService
from app.services.stock_query_service import StockQueryService


class StockTool:

    def __init__(
            self,
            stock_query_service: StockQueryService,
            stock_search_service: StockSearchService,
    ):
        self.stock_query_service = stock_query_service
        self.stock_search_service = stock_search_service

    def get_stock_price(self, stock_name: str) -> dict:
        """
        주식 현재가를 조회한다.

        Args:
            stock_name: 종목 이름
        """

        print("stock_price is used.")

        symbol = self.stock_search_service.find_symbol(stock_name)
        if symbol is None: return {"error": f"No data found for '{stock_name}'"}

        return self.stock_query_service.get_stock_price_for_agent(symbol)

    def get_stock_history(
        self,
        stock_name: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict]:
        """
        과거 주식 가격을 조회한다.

        Args:
            stock_name: 종목 이름
            start_date: YYYY-MM-DD (optional)
            end_date: YYYY-MM-DD (optional)
        """

        print("stock_history is used.")

        symbol = self.stock_search_service.find_symbol(stock_name)
        if symbol is None: return {"error": f"No data found for '{stock_name}'"}

        return self.stock_query_service.get_stock_history(symbol, start_date, end_date)

    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=self.get_stock_price,
                name="stock_price",
                description="""\
                주식 현재가를 조회한다.
                
                Args:
                stock_name: 종목 이름"""
            ),
            StructuredTool.from_function(
                func=self.get_stock_history,
                name="stock_history",
                description="""\
                과거 주식 가격을 조회한다.
                
                Args:
                stock_name: 종목 이름
                start_date: YYYY-MM-DD (optional)
                end_date: YYYY-MM-DD (optional)"""
            )
        ]
