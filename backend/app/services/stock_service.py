from fastapi import Depends

from app.repositories.postgres_stock_repository import get_stock_repository, StockRepository
import FinanceDataReader as fdr
from datetime import datetime

from app.clients.fdr_client import StockSymbolService


class StockService:

    def __init__(
            self,
            stock_repository: StockRepository,
            stock_symbol_service: StockSymbolService,
    ):
        self.stock_symbol_service = stock_symbol_service
        self.stock_repository = stock_repository

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


def get_stock_service(
        repository: StockRepository = Depends(get_stock_repository),
        stock_symbol_service: StockSymbolService = Depends(StockSymbolService),
):
    return StockService(repository, stock_symbol_service)