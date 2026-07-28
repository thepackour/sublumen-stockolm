from app.clients.fdr_client import StockSymbolService
from app.clients.gemini_embedding import GeminiEmbeddingClient
from app.clients.news_client import NewsClient
from app.core.database import SessionLocal
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository
from app.repositories.postgres_news_repository import NewsRepository
from app.services.news_query_service import NewsQueryService


class Container:

    def __init__(self):
        # clients
        self.stock_symbol_service = StockSymbolService()
        self.news_client = NewsClient()
        self.embedding_client = GeminiEmbeddingClient()

        # repositories
        self.news_repository = NewsRepository(SessionLocal)
        self.news_embedding_repository = NewsEmbeddingRepository(SessionLocal)

        # services
        self.news_query_service = NewsQueryService(
            self.news_repository,
            self.news_embedding_repository,
            self.news_client,
            self.stock_symbol_service,
            self.embedding_client
        )

    def initialize(self):
        self.stock_symbol_service.initialize()

    def shutdown(self):
        pass

container = Container()