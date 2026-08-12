from app.clients.fdr_client import FdrClient
from app.repositories.postgres_stock_repository import StockRepository
from datetime import datetime, timedelta

from app.services.stock_search_service import StockSearchService
from app.schemas import Stock


class StockQueryService:

    def __init__(
            self,
            stock_repository: StockRepository,
            stock_search_service: StockSearchService,
            fdr_client: FdrClient,
    ):
        self.stock_repository = stock_repository
        self.stock_search_service = stock_search_service
        self.fdr_client = fdr_client

    def get_stock_history(self, symbol, start_date = None, end_date = None):

        if start_date is None: 
            now = datetime.now()
            start_date = now.replace(year=now.year - 1).strftime("%Y-%m-%d")

        if end_date is None: df = self.fdr_client.get_stock_price(symbol, start_date)
        else: df = self.fdr_client.get_stock_price(symbol, start_date, end_date)
        
        if df.empty:
            return []
        
        return (
            df.reset_index()
            .rename(columns={"Date": "date"})
            .to_dict(orient="records")
        )

    def get_stock_price_for_agent(self, symbol: str) -> dict:

        today = datetime.now()
        yesterday = today - timedelta(days=1)

        df = self.fdr_client.get_stock_price(
            symbol,
            yesterday.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d")
        )

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
        return self.stock_repository.search_stocks_by_keyword(query, limit)

    def get_stock(self, symbol: str) -> Stock:
        return self.stock_repository.find_by_symbol(symbol)