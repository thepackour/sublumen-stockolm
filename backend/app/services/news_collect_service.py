from datetime import datetime
from email.utils import parsedate_to_datetime
from warnings import deprecated

from app.clients.fdr_client import StockSymbolService
from app.clients.news_client import NewsClient
from app.repositories.news_keyword_repository import NewsKeywordRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository
from app.repositories.postgres_news_repository import NewsRepository
from app.repositories.postgres_stock_repository import StockRepository
from app.services.news_embedding_service import NewsEmbeddingService


class NewsCollectService:
    def __init__(
            self,
            news_repository: NewsRepository,
            news_embedding_repository: NewsEmbeddingRepository,
            news_keyword_repository: NewsKeywordRepository,
            stock_repository: StockRepository,
            news_client: NewsClient,
            stock_symbol_service: StockSymbolService,
            news_embedding_service: NewsEmbeddingService,
    ):
        self.news_repository = news_repository
        self.news_embedding_repository = news_embedding_repository
        self.news_keyword_repository = news_keyword_repository
        self.stock_repository = stock_repository
        self.news_client = news_client
        self.stock_symbol_service = stock_symbol_service
        self.news_embedding_service = news_embedding_service

        self.last_collected_at: datetime = datetime.now()

    @deprecated("collect_news_with_priority()를 사용하세요.")
    def collect_news(self) -> dict:
        targets = self.news_keyword_repository.find_collect_targets(datetime.now())
        news = []
        for target in targets:
            data = self.news_client.get_news_by_news_keyword(target)

            symbol = self.stock_symbol_service.find_symbol(target.keyword)

            stock_id = None
            if symbol is not None:
                stock = self.stock_repository.find_by_symbol(symbol)
                if stock:
                    stock_id = stock.id

            for item in data:
                news.append(
                    {
                        "stock_id": stock_id,
                        "title": item["title"],
                        "content": item["description"], # 크롤러 도입하면 바꿀 예정
                        "summary": item["description"],
                        "url": item["originallink"],
                        "published_at": parsedate_to_datetime(item["pubDate"]),
                    }
                )
        saved_news = self.news_repository.save_all(news)
        embeddings = []
        for n in saved_news: embeddings.extend(self.news_embedding_service.embed_news(n))
        self.news_embedding_repository.save_all(embeddings)

        return {"news_count": len(saved_news), "embeddings_count": len(embeddings)}

    def collect_news_with_priority(self, priority: int) -> dict:
        targets = self.news_keyword_repository.find_targets_by_priority(priority)
        news = []
        for target in targets:
            data = self.news_client.get_news_by_news_keyword(target)

            symbol = self.stock_symbol_service.find_symbol(target.keyword)

            stock_id = None
            if symbol is not None:
                stock = self.stock_repository.find_by_symbol(symbol)
                if stock:
                    stock_id = stock.id

            for item in data:
                news.append(
                    {
                        "stock_id": stock_id,
                        "title": item["title"],
                        "content": item["description"], # 크롤러 도입하면 바꿀 예정
                        "summary": item["description"],
                        "url": item["originallink"],
                        "published_at": parsedate_to_datetime(item["pubDate"]),
                    }
                )
        saved_news = self.news_repository.save_all(news)
        embeddings = []
        for n in saved_news: embeddings.extend(self.news_embedding_service.embed_news(n))
        self.news_embedding_repository.save_all(embeddings)

        return {"news_count": len(saved_news), "embeddings_count": len(embeddings)}

    def collect_latest_news_for_agent(
            self,
            keyword: str,
            limit
    ) -> str:
        news_list = self.news_client.get_news_by_keyword(keyword, limit)

        contexts = []
        for news in news_list:
            contexts.append(
                f"""
                [뉴스]
    
                제목:
                {news["title"]}
    
                요약:
                {news["description"]}
    
                발행일:
                {news["pubDate"]}
    
                URL:
                {news["originallink"]}
                """
            )

        return "\n\n".join(contexts)
