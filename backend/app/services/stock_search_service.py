from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.clients.kis_client import KisApiClient


class StockSearchService:

    def __init__(
            self,
            kis_client: KisApiClient
    ):
        self.kis_client = kis_client

    def find_symbol(self, keyword: str) -> str:
        if not keyword or not keyword.isdigit() or len(keyword) != 6:
            raise ProjectException(ErrorCode.STOCK404_1)
        if not self.kis_client.search_stock(keyword):
            raise ProjectException(ErrorCode.STOCK404_1)
        return keyword
