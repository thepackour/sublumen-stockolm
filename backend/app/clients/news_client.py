import requests

from app.core.config import settings
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException
from app.core.logger import logger
from enum import Enum

from app.schemas.news_keyword import NewsKeyword


class Sort(Enum):
    ACC = "sim"  # 정확도 기준 내림차순
    DATE = "date"  # 날짜 기준 내림차순

class NewsClient:

    def get_news_by_query(
        self,
        query: str,
        size: int = 20,
        sort: Sort = Sort.ACC,
        cursor: int = 1,
    ) -> list:

        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            params={
                "query": query,
                "display": size,
                "start": cursor,
                "sort": sort.value,
            },
            headers={
                "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            },
        )

        data = response.json()

        if response.status_code >= 500:
            logger.error(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS500_1)

        if response.status_code >= 400:
            logger.warning(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS400_1)

        logger.info(
            "뉴스 조회 API (%s): %d개 조회",
            response.status_code,
            len(data["items"]),
        )

        return data["items"]

    def get_news_by_news_keyword(
        self,
        news_keyword: NewsKeyword,
        size: int = 20
    ) -> list:

        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            params={
                "query": news_keyword.keyword,
                "display": size,
                "sort": Sort.DATE.value,
            },
            headers={
                "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            },
        )

        data = response.json()

        if response.status_code >= 500:
            logger.error(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS500_1)

        if response.status_code >= 400:
            logger.warning(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS400_1)

        logger.info(
            "뉴스 조회 API (%s): %d개 조회",
            response.status_code,
            len(data["items"]),
        )

        return data["items"]

    def get_news_by_keyword(
        self,
        keyword: str,
        size: int = 10
    ) -> list:
        if size > 10: size = 10

        response = requests.get(
            "https://openapi.naver.com/v1/search/news.json",
            params={
                "query": keyword,
                "display": size,
                "sort": Sort.DATE.value,
            },
            headers={
                "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            },
        )

        data = response.json()

        if response.status_code >= 500:
            logger.error(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS500_1)

        if response.status_code >= 400:
            logger.warning(
                "뉴스 조회 API (%s): %s",
                response.status_code,
                data.get("errorMessage"),
            )
            raise ProjectException(ErrorCode.NEWS400_1)

        logger.info(
            "뉴스 조회 API (%s): %d개 조회",
            response.status_code,
            len(data["items"]),
        )

        return data["items"]