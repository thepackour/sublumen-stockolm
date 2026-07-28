from fastapi import Request

import FinanceDataReader as fdr
import pandas as pd


class StockSymbolService:

    def __init__(self):
        self.stocks = None

    def initialize(self):
        krx = fdr.StockListing("KRX").rename(columns={"Code": "Symbol"})
        nasdaq = fdr.StockListing("NASDAQ")

        self.stocks = pd.concat([krx, nasdaq], ignore_index=True)

    def find_symbol(self, keyword):
        result = self.search_stock(keyword)

        if result.empty:
            return None

        return result.iloc[0]["Symbol"]

    def search_stock(self, keyword, limit = None):
        result = self.stocks[
            self.stocks["Name"].str.contains(keyword, case=False, na=False)
        ]

        return result[:limit]

    def get_stock(self, symbol):
        return self.stocks[self.stocks["Symbol"] == symbol]


def get_stock_symbol_service(
        request: Request,
) -> StockSymbolService:
    return request.app.state.stock_symbol_service