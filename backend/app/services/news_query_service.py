from app.clients.fdr_client import StockSymbolService
from app.clients.gemini_embedding import EmbeddingClient
from app.dto.response.news_response import NewsResponse
from app.dto.response.page_response import PageResponse
from app.repositories.postgres_news_repository import NewsRepository
from app.repositories.postgres_news_embedding_repository import NewsEmbeddingRepository


class NewsQueryService:

    def __init__(
            self,
            news_repository: NewsRepository,
            news_embedding_repository: NewsEmbeddingRepository,
            stock_symbol_service: StockSymbolService,
            embedding_client: EmbeddingClient
    ):
        self.news_repository = news_repository
        self.news_embedding_repository = news_embedding_repository
        self.stock_symbol_service = stock_symbol_service
        self.embedding_client = embedding_client

    def get_news_by_keyword(self, keyword: str, page: int = 1, size: int = 10) -> PageResponse[NewsResponse]:
        query = self.embedding_client.embed_keyword(keyword)
        tmp, total = self.news_embedding_repository.search_news_id_by_embedding(query.values, page, size)
        news_ids = [item[0] for item in tmp]
        news_list = self.news_repository.find_all_by_ids(news_ids)
        news_map = {
            news.id: news
            for news in news_list
        }

        items = [NewsResponse(
            news_id=id,
            title=news_map[id]["title"],
            summary=news_map[id]["summary"],
            source=news_map[id]["source"],
            url=news_map[id]["url"],
            published_at=news_map[id]["published_at"],

            related_stock_id=news_map[id]["stock_id"],
            related_stock_name=self.stock_symbol_service.get_stock(news_map[id]["symbol"])["stock_name"],
        )
            for id in news_ids
        ]

        return PageResponse(
            items=items,
            count=len(items),
            page=page,
            size=size,
            total_count=total
        )


    def get_news_by_stock_name(self, stock_name: str, page: int = 1, size: int = 10):
        symbol = self.stock_symbol_service.find_symbol(stock_name)
        stock = self.stock_symbol_service.get_stock(symbol)
        result = self.news_repository.find_latest_by_stock_id(stock.id, page, size)
        return result