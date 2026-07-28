from datetime import datetime
from email.utils import parsedate_to_datetime

from app.clients.fdr_client import StockSymbolService
from app.clients.gemini_embedding import GeminiEmbeddingClient
from app.clients.news_client import NewsClient
from app.container import container
from app.repositories.news_keyword_repository import NewsKeywordRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository, get_news_embedding_repository
from app.repositories.postgres_news_repository import NewsRepository, get_news_repository
from app.repositories.postgres_stock_repository import StockRepository
from app.schemas import News


class NewsCollectService:
    def __init__(
            self,
            news_repository: NewsRepository,
            news_embedding_repository: NewsEmbeddingRepository,
            news_keyword_repository: NewsKeywordRepository,
            stock_repository: StockRepository,
            news_client: NewsClient,
            stock_symbol_service: StockSymbolService,
            embedding_client: GeminiEmbeddingClient,
    ):
        self.news_repository = news_repository
        self.news_embedding_repository = news_embedding_repository
        self.news_keyword_repository = news_keyword_repository
        self.stock_repository = stock_repository
        self.news_client = news_client
        self.stock_symbol_service = stock_symbol_service
        self.embedding_client = embedding_client

    def collect_news(self):
        targets = self.news_keyword_repository.find_collect_targets(datetime.now())
        news = []
        for target in targets:
            data = self.news_client.get_news_by_news_keyword(target)
            stock_name = self.stock_symbol_service.search_stock(target)
            symbol = self.stock_symbol_service.get_stock(stock_name)["symbol"]
            stock_id = None
            if symbol is not None:
                stock_id = self.stock_repository.find_by_symbol(symbol).id
            for item in data:
                news.append(News(
                    stock_id=stock_id,
                    title=item["title"],
                    content=item["description"],  # 크롤러 도입하면 원문으로 대체
                    url=item["originallink"],
                    published_at=parsedate_to_datetime(item["pubDate"]),
                ))
        self.news_repository.save_all(news)


def get_news_collect_service():
    return NewsCollectService(
        container.news_repository,
        container.news_embedding_repository,
        container.news_keyword_repository,
        container.stock_repository,
        container.news_client,
        container.stock_symbol_service,
        container.embedding_client,
    )