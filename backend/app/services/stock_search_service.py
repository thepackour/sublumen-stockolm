from difflib import SequenceMatcher
from threading import Lock
from time import monotonic
from typing import Callable, Optional

from app.clients.fdr_client import FdrClient
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.dto.StockInfo import StockInfo


class StockSearchService:

    def __init__(
            self,
            fdr_client: FdrClient,
            cache_ttl_seconds: int = 24 * 60 * 60,
            clock: Callable[[], float] = monotonic,
    ):
        self.fdr_client = fdr_client
        self.cache_ttl_seconds = cache_ttl_seconds
        self.clock = clock
        self._stocks: tuple[StockInfo, ...] = ()
        self._loaded_at = 0.0
        self._lock = Lock()

    @staticmethod
    def _normalize(value: str) -> str:
        return "".join(character.lower() for character in value if character.isalnum())

    def _catalog(self) -> tuple[StockInfo, ...]:
        now = self.clock()
        if self._stocks and now - self._loaded_at < self.cache_ttl_seconds:
            return self._stocks

        with self._lock:
            now = self.clock()
            if not self._stocks or now - self._loaded_at >= self.cache_ttl_seconds:
                self._stocks = tuple(self.fdr_client.get_stock_list())
                self._loaded_at = now
        return self._stocks

    def search(self, keyword: str | None, limit: int = 10) -> list[StockInfo]:
        if limit < 1 or not keyword or not keyword.strip():
            return []

        stocks = self._catalog()
        normalized_keyword = self._normalize(keyword)

        def score(stock: StockInfo) -> tuple[float, float, str]:
            normalized_name = self._normalize(stock.name)
            normalized_symbol = self._normalize(stock.symbol)

            if normalized_keyword == normalized_symbol:
                match_score = 5.0
            elif normalized_keyword == normalized_name:
                match_score = 4.0
            elif normalized_name.startswith(normalized_keyword):
                match_score = 3.0
            elif normalized_keyword in normalized_name:
                match_score = 2.0
            else:
                match_score = SequenceMatcher(
                    None, normalized_keyword, normalized_name
                ).ratio()

            similarity = SequenceMatcher(
                None, normalized_keyword, normalized_name
            ).ratio()
            return match_score, similarity, stock.name

        ranked = sorted(
            ((score(stock), stock) for stock in stocks),
            key=lambda item: item[0],
            reverse=True,
        )
        return [
            stock
            for stock_score, stock in ranked
            if stock_score[0] >= 2.0 or stock_score[1] >= 0.45
        ][:limit]

    def find_by_symbol(self, symbol: str) -> StockInfo:
        normalized_symbol = self._normalize(symbol)
        for stock in self._catalog():
            if self._normalize(stock.symbol) == normalized_symbol:
                return stock
        raise ProjectException(ErrorCode.STOCK404_1)

    def find_symbol(self, keyword: str) -> Optional[str]:
        result = self.search(keyword, limit=1)

        if not result:
            raise ProjectException(ErrorCode.STOCK404_1)

        return result[0].symbol
