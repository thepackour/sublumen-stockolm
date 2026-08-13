from typing import Optional

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.repositories.postgres_stock_repository import StockRepository


class StockSearchService:

    def __init__(
            self,
            stock_repository: StockRepository
    ):
        self.stock_repository = stock_repository

    def find_symbol(self, keyword: str) -> Optional[str]:
        result = self.stock_repository.search_stocks_by_keyword(keyword)

        if len(result) == 0:
            raise ProjectException(ErrorCode.STOCK404_1)

        return result[0].symbol