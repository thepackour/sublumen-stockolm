import pandas as pd

from app.clients.fdr_client import StockSymbolService
from app.repositories.postgres_stock_repository import StockRepository
from app.schemas import Stock

market_currency_table = {
    "KRX": "KRW",
    "NASDAQ": "USD"
}


class StockCollectService:

    def __init__(
            self,
            stock_repository: StockRepository,
            stock_symbol_service: StockSymbolService,
    ):
        self.stock_repository = stock_repository
        self.stock_symbol_service = stock_symbol_service

    def initialize(self):
        self.stock_symbol_service.initialize()
        stock_list = [
            Stock(
                symbol=row.Symbol,
                name=row.Name,
                market=row.Market,
                sector=row.Sector,
                industry=row.Industry,
                is_domestic=row.Market in ["KRX"],
                currency=market_currency_table[row.Market]
            )
            for row in self.stock_symbol_service.stocks.itertuples()
        ]
        stocks = self.stock_repository.save_all(stock_list)
        df = pd.DataFrame([
            {
                "StockId": stock.id,
                "Symbol": stock.symbol,
                "IsDomestic": stock.is_domestic,
                "Currency": stock.currency
            }
            for stock in stocks
        ])
        self.stock_symbol_service.stocks = self.stock_symbol_service.stocks.merge(
            df, on="Symbol", how="left"
        )