from app.repositories.mock_news_repository import NewsRepository

repository = NewsRepository()


class NewsService:

    def get_news(self, query: str, stock: str = None, page: int = 1, size: int = 10):
        return repository.get_news(query=query, stock=stock, page=page, size=size)