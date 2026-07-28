from app.clients.fdr_client import StockSymbolService
from app.clients.gemini_embedding import GeminiEmbeddingClient
from app.repositories.postgres_news_repository import NewsRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository


class NewsQueryService:

    def __init__(
            self,
            news_repository: NewsRepository,
            news_embedding_repository: NewsEmbeddingRepository,
            stock_symbol_service: StockSymbolService,
            embedding_client: GeminiEmbeddingClient
    ):
        self.news_repository = news_repository
        self.news_embedding_repository = news_embedding_repository
        self.stock_symbol_service = stock_symbol_service
        self.embedding_client = embedding_client

    def get_news_by_keyword(self, keyword: str, page: int = 1, size: int = 10):
        query = self.embedding_client.embed_query(keyword)
        tmp = self.news_embedding_repository.search_news_id_by_embedding(query, page, size)
        news_ids = [item[0] for item in tmp]
        news_list = self.news_repository.find_all_by_ids(news_ids)
        news_map = {
            news.id: news
            for news in news_list
        }
        result = [
            news_map[id]
            for id in news_ids
        ]
        return result


    def get_news_by_stock_name(self, stock_name: str, page: int = 1, size: int = 10):
        symbol = self.stock_symbol_service.find_symbol(stock_name)
        stock = self.stock_symbol_service.get_stock(symbol)
        result = self.news_repository.find_latest_by_stock_id(stock.id, page, size)
        return result