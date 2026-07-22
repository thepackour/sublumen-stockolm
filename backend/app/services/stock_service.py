from app.repositories.mock_stock_repository import StockRepository
import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime

repository = StockRepository()


class StockService:

    def __init__(self):
        krx = fdr.StockListing("KRX").rename(columns={"Code": "Symbol"})
        nasdaq = fdr.StockListing("NASDAQ")

        self.stocks = pd.concat([krx, nasdaq], ignore_index=True)

    def search_stock(self, keyword, limit = None):
        result = self.stocks[
            self.stocks["Name"].str.contains(keyword, case=False, na=False)
        ]

        return result[:limit]
        # return repository.search(keyword, limit)

    def get_stock(self, symbol):
        return self.stocks[self.stocks["Symbol"] == symbol]
        # return repository.find(symbol)

    def find_symbol(self, keyword):
        result = self.search_stock(keyword)

        if result.empty:
            return None

        return result.iloc[0]["Symbol"]

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