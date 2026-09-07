from __future__ import annotations

from datetime import date, timedelta

from app.clients.kis_client import KisApiClient
from app.clients.kis_websocket import KisRealtimeClient
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.services.stock_search_service import StockSearchService


class StockQueryService:
    def __init__(self, kis_client: KisApiClient, stock_search_service: StockSearchService):
        self.kis_client = kis_client
        self.stock_search_service = stock_search_service
        self.realtime_client = KisRealtimeClient(kis_client)

    def resolve(self, query: str) -> str:
        return self.stock_search_service.find_symbol(query)

    def get_stock_history(self, symbol: str, start_date: str | None = None, end_date: str | None = None):
        symbol = self.resolve(symbol)
        end = end_date or date.today().isoformat()
        start = start_date or (date.today() - timedelta(days=365)).isoformat()
        return [self._normalize_history(row) for row in self.kis_client.get_history(symbol, start, end)]

    @staticmethod
    def _number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _normalize_history(self, row: dict) -> dict:
        return {"date": row.get("stck_bsop_date"), "open": self._number(row.get("stck_oprc")), "high": self._number(row.get("stck_hgpr")), "low": self._number(row.get("stck_lwpr")), "close": self._number(row.get("stck_clpr")), "volume": self._number(row.get("acml_vol")), "turnover": self._number(row.get("acml_tr_pbmn"))}

    def get_stock_price_for_agent(self, symbol: str) -> dict:
        symbol = self.resolve(symbol)
        row = self.kis_client.get_price(symbol)
        if not row:
            raise ProjectException(ErrorCode.STOCK404_1)
        return {"symbol": symbol, "name": row.get("hts_kor_isnm"), "date": date.today().isoformat(), "open": self._number(row.get("stck_oprc")), "high": self._number(row.get("stck_hgpr")), "low": self._number(row.get("stck_lwpr")), "close": self._number(row.get("stck_prpr")), "volume": self._number(row.get("acml_vol")), "change": self._number(row.get("prdy_vrss")), "change_rate": self._number(row.get("prdy_ctrt"))}

    def get_stock(self, query: str) -> dict:
        return self.kis_client.search_stock(self.resolve(query))

    def get_financial(self, query: str) -> dict:
        symbol = self.resolve(query)
        return {"symbol": symbol, "data": self.kis_client.get_financial(symbol)}
