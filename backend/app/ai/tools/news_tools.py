from langchain_core.tools import StructuredTool

from app.services.news_collect_service import NewsCollectService
from app.services.news_query_service import NewsQueryService


class NewsTool:

    def __init__(
            self,
            news_query_service: NewsQueryService,
            news_collect_service: NewsCollectService,
    ):
        self.news_query_service = news_query_service
        self.news_collect_service = news_collect_service

    def search_news(
        self,
        keyword: str,
        limit: int = 5,
    ) -> str:
        """
        키워드와 관련된 뉴스를 저장된 데이터 중에서 관련도 순으로 검색한다.

        Args:
            keyword:
                검색할 뉴스 키워드

            limit:
                검색할 뉴스 개수
        """
        print("search_news is used.")

        return self.news_query_service.retrieve_news_for_agent(
            keyword,
            limit,
        )

    def search_latest_news(
            self,
            keyword: str,
            limit: int = 5,
    ):
        """
        키워드와 관련된 뉴스를 최신 순으로 검색한다.

        Args:
            keyword:
                검색할 뉴스 키워드

            limit:
                검색할 뉴스 개수 (1~20)
        """
        print("search_latest_news is used.")

        return self.news_collect_service.collect_latest_news_for_agent(
            keyword,
            limit
        )


    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=self.search_news,
                name="search_news",
                description=
                """
                        키워드와 관련된 뉴스를 저장된 데이터 중에서 관련도 순으로 검색한다.
        
                        Args:
                            keyword:
                                검색할 뉴스 키워드
        
                            limit:
                                검색할 뉴스 개수
                        """
            ),
            StructuredTool.from_function(
                func=self.search_latest_news,
                name="search_latest_news",
                description=
                """
                        키워드와 관련된 뉴스를 최신 순으로 검색한다.
        
                        Args:
                            keyword:
                                검색할 뉴스 키워드
        
                            limit:
                                검색할 뉴스 개수 (1~20)
                        """
            )
        ]
