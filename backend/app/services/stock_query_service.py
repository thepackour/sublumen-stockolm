from app.repositories.postgres_stock_repository import StockRepository
import FinanceDataReader as fdr
from datetime import datetime

from app.clients.fdr_client import StockSymbolService
from app.schemas import Stock


class StockQueryService:

    def __init__(
            self,
            stock_repository: StockRepository,
            stock_symbol_service: StockSymbolService,
    ):
        self.stock_repository = stock_repository
        self.stock_symbol_service = stock_symbol_service

    def get_stock_history(self, symbol, start_date = None, end_date = None):

        if start_date is None: 
            now = datetime.now()
            start_date = now.replace(year=now.year - 1).strftime("%Y-%m-%d")

        if end_date is None: df = fdr.DataReader(symbol, start_date)
        else: df = fdr.DataReader(symbol, start_date, end_date)
        
        if df.empty:
            return []
        
        return (
            df.reset_index()
            .rename(columns={"Date": "date"})
            .to_dict(orient="records")
        )

    def get_stock_price(self, symbol: str) -> dict:

        df = fdr.DataReader(symbol)

        latest = df.iloc[-1]

        if len(df) >= 2:
            previous_close = df.iloc[-2]["Close"]
            current_close = latest["Close"]

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
        stocks = self.stock_symbol_service.search_stock(query, limit)
        stock_ids = [stock["StockId"] for stock in stocks]
        return self.stock_repository.find_all_by_stock_ids(stock_ids)

    def get_stock(self, symbol: str) -> Stock:
        stock = self.stock_symbol_service.get_stock(symbol)
        return self.stock_repository.find(stock["StockId"])