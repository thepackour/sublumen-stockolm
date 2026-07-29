from typing import Optional

import FinanceDataReader as fdr
import pandas as pd


class StockSymbolService:

    def __init__(self):
        self.stocks = None

    def initialize(self):
        krx = fdr.StockListing("KRX").rename(columns={"Code": "Symbol"})
        nasdaq = fdr.StockListing("NASDAQ")

        self.stocks = pd.concat([krx, nasdaq], ignore_index=True)

    def find_symbol(self, keyword: str) -> Optional[str]:
        result = self.search_stock(keyword)

        if len(result) == 0:
            return None

        return result[0]["Symbol"]

    def search_stock(self, keyword: str, limit = None) -> list[dict]:
        result = self.stocks[
            self.stocks["Name"].str.contains(keyword, case=False, na=False)
        ]

        return result[:limit]

    def get_stock(self, symbol: str):
        return self.stocks[self.stocks["Symbol"] == symbol]

    def get_stock_by_stock_id(self, stock_id: int):
        return self.stocks[self.stocks["StockId"] == stock_id]