from fastapi import Depends

from app.services.stock_service import get_stock_service, StockService


class StockSymbolUtil:

    def __init__(self, stock_service: StockService):
        self.stock_service = Depends(get_stock_service)

    def find_symbol(self, keyword):
        result = self.stock_service.search_stock(keyword)

        if result.empty:
            return None

        return result.iloc[0]["Symbol"]