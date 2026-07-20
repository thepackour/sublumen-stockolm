from app.repositories.mock_stock_repository import StockRepository

repository = StockRepository()


class StockService:

    def search_stock(self, keyword, limit):
        return repository.search(keyword, limit)

    def get_stock(self, symbol):
        return repository.find(symbol)