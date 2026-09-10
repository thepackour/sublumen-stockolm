from app.ai.tools import FinancialStatementTool, StockTool
from app.ai.tools.news_tools import NewsTool
from app.clients.dart_client import DartClient
from app.clients.fdr_client import FdrClient
from app.services.stock_search_service import StockSearchService
from app.clients.gemini_embedding import EmbeddingClient
from app.clients.news_client import NewsClient
from app.core.config import settings
from app.core.database import SessionLocal
from app.repositories.news_keyword_repository import NewsKeywordRepository
from app.repositories.corp_info_repository import CorpInfoRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository
from app.repositories.postgres_news_repository import NewsRepository
from app.services.exchange_rate_service import ExchangeRateService
from app.services.financial_statement_service import FinancialStatementService
from app.services.news_collect_service import NewsCollectService
from app.services.news_embedding_service import NewsEmbeddingService
from app.services.news_query_service import NewsQueryService
from app.services.stock_query_service import StockQueryService


class Container:

    def __init__(self):

        # repositories
        self.news_repository = NewsRepository(SessionLocal)
        self.news_embedding_repository = NewsEmbeddingRepository(SessionLocal)
        self.news_keyword_repository = NewsKeywordRepository(SessionLocal)
        self.corp_info_repository = CorpInfoRepository(SessionLocal)

        # clients
        self.news_client = NewsClient()
        self.dart_client = DartClient(
            settings.DART_API_KEY,
            settings.DART_BASE_URL,
            settings.DART_TIMEOUT_SECONDS,
        )
        self.embedding_client = EmbeddingClient()
        self.fdr_client = FdrClient()
        self.stock_search_service = StockSearchService(
            self.fdr_client,
            settings.STOCK_CATALOG_CACHE_TTL_SECONDS,
        )

        # services
        self.news_embedding_service = NewsEmbeddingService(
            self.embedding_client
        )
        self.stock_query_service = StockQueryService(
            self.stock_search_service,
            self.fdr_client,
        )
        self.exchange_rate_service = ExchangeRateService(self.fdr_client)
        self.financial_statement_service = FinancialStatementService(
            self.dart_client,
            self.corp_info_repository,
        )
        self.news_query_service = NewsQueryService(
            self.news_repository,
            self.news_embedding_repository,
            self.stock_search_service,
            self.embedding_client
        )
        self.news_collect_service = NewsCollectService(
            self.news_repository,
            self.news_embedding_repository,
            self.news_keyword_repository,
            self.news_client,
            self.news_embedding_service,
            self.stock_search_service,
        )

        # tools
        self.stock_tool = StockTool(
            self.stock_query_service,
            self.stock_search_service,
        )
        self.news_tool = NewsTool(
            self.news_query_service,
            self.news_collect_service,
        )
        self.financial_statement_tool = FinancialStatementTool(
            self.financial_statement_service
        )


    def initialize(self):
        # self.news_keyword_repository.initialize()
        pass

    def shutdown(self):
        pass

container = Container()
