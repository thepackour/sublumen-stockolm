from warnings import deprecated

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.repositories.postgres_stock_repository import StockRepository


@deprecated("StockRepository의 search_stocks_by_keyword()를 사용하세요.")
class StockSearchService:

    def __init__(
            self,
            stock_repository: StockRepository
    ):
        self.stock_repository = stock_repository

    def find_symbol(self, keyword: str, limit: int = 1) -> list[str]:
        """
        키워드와 가장 유사한

        Args:
            keyword:
            limit:

        Returns:

        """
        result = self.stock_repository.search_stocks_by_keyword(keyword, limit)

        if len(result) == 0:
            raise ProjectException(ErrorCode.STOCK404_1)

        return [stock.symbol for stock in result]