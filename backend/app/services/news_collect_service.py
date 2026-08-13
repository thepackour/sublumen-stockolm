from datetime import datetime
from email.utils import parsedate_to_datetime
from warnings import deprecated

from app.clients.news_client import NewsClient
from app.core.logger import logger
from app.repositories.news_keyword_repository import NewsKeywordRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository
from app.repositories.postgres_news_repository import NewsRepository
from app.services.crawlers.crawler_factory import CrawlerFactory
from app.services.news_embedding_service import NewsEmbeddingService


class NewsCollectService:
    def __init__(
            self,
            news_repository: NewsRepository,
            news_embedding_repository: NewsEmbeddingRepository,
            news_keyword_repository: NewsKeywordRepository,
            news_client: NewsClient,
            news_embedding_service: NewsEmbeddingService,
    ):
        self.news_repository = news_repository
        self.news_embedding_repository = news_embedding_repository
        self.news_keyword_repository = news_keyword_repository
        self.news_client = news_client
        self.news_embedding_service = news_embedding_service

        self.last_collected_at: datetime = datetime.now()

    @deprecated("collect_news_with_priority()를 사용하세요.")
    def collect_news(self) -> dict:
        targets = self.news_keyword_repository.find_collect_targets(datetime.now())
        news = []
        for target in targets:
            data = self.news_client.get_news_by_news_keyword(target)

            # 한국투자증권 API에 맞춰서 바꿔야 함!!!
            stock = {
                "ticker": "123456",
                "name": "ㅇㅇ주식회사"
            }
            if not stock:
                logger.info(
                    "collect_news: No related stocks with the keyword (%s)\n",
                    target
                )

            crawlers = CrawlerFactory()
            for item in data:
                article = None
                try:
                    crawler = crawlers.get_crawler(item["originallink"])
                    article = crawler.get_article(item["originallink"])
                except AttributeError as e:
                    logger.error(
                        "Crawler Error: Cannot parse the article (%s)\n%s",
                        item["originallink"],
                        str(e.obj)
                    )
                news.append(
                    {
                        "title": item["title"],
                        "content": item["description"] if article is None else article,
                        "summary": item["description"], # 요약하는 기능 구현하면 사용하면 바꿀 예정
                        "url": item["originallink"],
                        "published_at": parsedate_to_datetime(item["pubDate"]),
                        "stock_ticker": None if stock is None else stock["ticker"],
                        "stock_name": None if stock is None else stock["name"]
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

            # 한국투자증권 API에 맞춰서 바꿔야 함!!!
            stock = {
                "ticker": "123456",
                "name": "ㅇㅇ주식회사"
            }
            if not stock:
                logger.info(
                    "collect_news_with_priority: No related stocks with the keyword (%s)\n",
                    target
                )

            for item in data:
                news.append(
                    {
                        "title": item["title"],
                        "content": item["description"], # 크롤러 도입하면 바꿀 예정
                        "summary": item["description"],
                        "url": item["originallink"],
                        "published_at": parsedate_to_datetime(item["pubDate"]),
                        "stock_ticker": None if stock is None else stock["ticker"],
                        "stock_name": None if stock is None else stock["name"]
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
            limit = 10
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
