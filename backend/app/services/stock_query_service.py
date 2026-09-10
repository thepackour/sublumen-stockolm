from app.clients.fdr_client import FdrClient
from datetime import datetime, timedelta

import pandas as pd

from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.services.stock_search_service import StockSearchService


class StockQueryService:

    def __init__(
            self,
            stock_search_service: StockSearchService,
            fdr_client: FdrClient,
    ):
        self.stock_search_service = stock_search_service
        self.fdr_client = fdr_client

    def get_stock_history(self, symbol, start_date = None, end_date = None):

        if start_date is None: 
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        try:
            if end_date is None:
                df = self.fdr_client.get_stock_price(symbol, start_date)
            else:
                df = self.fdr_client.get_stock_price(symbol, start_date, end_date)
        except Exception as exc:
            raise ProjectException(ErrorCode.STOCK404_1) from exc
        
        return self._price_records(df)

    def get_stock_price_for_agent(self, symbol: str) -> dict:

        today = datetime.now()
        start = today - timedelta(days=10)

        try:
            df = self.fdr_client.get_stock_price(
                symbol,
                start.strftime("%Y-%m-%d"),
                today.strftime("%Y-%m-%d")
            )
        except Exception as exc:
            raise ProjectException(ErrorCode.STOCK404_1) from exc

        if df.empty:
            raise ProjectException(ErrorCode.STOCK404_1)

        latest = df.iloc[-1]
        change = float(latest.get("Change", 0.0)) * 100
        if len(df) >= 2:
            previous_close = df.iloc[-2]["Close"]
            current_close = latest["Close"]
            if previous_close:
                change = ((current_close - previous_close) / previous_close) * 100

        return {
            "symbol": symbol,
            "date": str(df.index[-1].date()),
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "close": float(latest["Close"]),
            "volume": int(latest["Volume"]),
            "change": round(change, 2),
        }

    def search_stock(self, query: str, limit: int = 10):
        return self.stock_search_service.search(query, limit)

    def get_stock(self, symbol: str):
        return self.stock_search_service.find_by_symbol(symbol)

    @staticmethod
    def _price_records(df) -> list[dict]:
        records = []
        for index, row in df.iterrows():
            record = {
                "date": index.date().isoformat() if hasattr(index, "date") else str(index),
            }
            for column, value in row.items():
                key = str(column).lower().replace(" ", "_")
                if pd.isna(value):
                    record[key] = None
                elif key == "volume":
                    record[key] = int(value)
                else:
                    record[key] = float(value)
            records.append(record)
        return records
