from app.clients.fdr_client import FdrClient
from app.repositories.postgres_stock_repository import StockRepository
from app.schemas import Stock

market_currency_table = {
    "KRX": "KRW",
    "KOSDAQ": "KRW",
    "KOSPI": "KRW",
    "KOSDAQ GLOBAL": "KRW",
    "KONEX": "KRW",
    "NASDAQ": "USD",
    "nan": None
}


class StockCollectService:

    def __init__(
        self,
        stock_repository: StockRepository,
        fdr_client: FdrClient,
    ):
        self.stock_repository = stock_repository
        self.fdr_client = fdr_client

    def initialize(self):
        stocks = self.stock_repository.find_all()

        if stocks:
            return

        stock_infos = self.fdr_client.get_stock_list()

        stocks = [
            Stock(
                symbol=info.symbol,
                name=info.name,
                market=info.market,
                sector=info.sector,
                industry=info.industry,
                is_domestic=info.market in ["KRX"],
                currency=market_currency_table.get(info.market),
            )
            for info in stock_infos
            if info.market is not None
        ]

        self.stock_repository.save_all(stocks)