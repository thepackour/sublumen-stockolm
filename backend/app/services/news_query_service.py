from app.clients.fdr_client import StockSymbolService
from app.clients.openai_embedding import EmbeddingClient
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

    def get_news_by_keyword(
            self,
            keyword: str,
            page: int = 1,
            size: int = 10
    ) -> PageResponse[NewsResponse]:
        query = self.embedding_client.embed_keyword(keyword)
        tmp, total = self.news_embedding_repository.search_news_id_by_embedding(
            query,
            page,
            size
        )
        news_ids = [item[0] for item in tmp]
        news_list = self.news_repository.find_all_by_ids(news_ids)
        news_map = {
            news.id: news
            for news in news_list
        }

        items = [NewsResponse(
            news_id=id,
            title=news_map[id].title,
            summary= news_map[id].summary,
            url=news_map[id].url,
            published_at=news_map[id].published_at,

            related_stock_id=news_map[id].stock_id,
            related_stock_name="" if news_map[id].stock_id is None else self.stock_symbol_service.get_stock_by_stock_id(news_map[id].stock_id)["Name"],
        )
            for id in news_ids
        ]

        return PageResponse[NewsResponse](
            items=items,
            count=len(items),
            page=page,
            size=size,
            total_count=total
        )

    def retrieve_news_for_agent(
            self,
            keyword: str,
            limit: int = 5,
    ) -> str:
        """
        키워드와 관련된 뉴스를 검색한다.
        LLM Agent가 참고할 뉴스 context를 반환한다.
        """

        query = self.embedding_client.embed_keyword(keyword)

        results, _ = self.news_embedding_repository.search_news_id_by_embedding(
            query,
            1,
            limit,
        )

        news_ids = [item[0] for item in results]

        news_list = self.news_repository.find_all_by_ids(news_ids)

        news_map = {
            news.id: news
            for news in news_list
        }

        contexts = []

        for news_id in news_ids:
            news = news_map.get(news_id)

            if news is None:
                continue

            stock_name = ""

            if news.stock_id:
                stock = self.stock_symbol_service.get_stock_by_stock_id(
                    news.stock_id
                )
                stock_name = stock["Name"]

            contexts.append(
                f"""
    [뉴스]

    제목:
    {news.title}

    요약:
    {news.summary}

    관련 종목:
    {stock_name}

    발행일:
    {news.published_at}

    URL:
    {news.url}
    """
            )

        return "\n\n".join(contexts)


    def get_news_by_stock_name(self, stock_name: str, page: int = 1, size: int = 10):
        symbol = self.stock_symbol_service.find_symbol(stock_name)
        stock = self.stock_symbol_service.get_stock(symbol)
        result = self.news_repository.find_latest_by_stock_id(stock["StockId"], page, size)
        return result