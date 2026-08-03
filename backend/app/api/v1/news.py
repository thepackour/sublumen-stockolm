from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse

from app.container import container
from app.core.response import success
from app.core.success_code import SuccessCode
from app.services.news_collect_service import NewsCollectService
from app.services.news_query_service import NewsQueryService


router = APIRouter(
    prefix="/api/v1/news",
    tags=["News"]
)

def get_news_collect_service():
    return container.news_collect_service

def get_news_query_service():
    return container.news_query_service

@router.get("")
def get_news(
        query: str = Query(..., description="검색어"),
        page: int = Query(1, description="페이지 번호"),
        size: int = Query(10, description="페이지당 뉴스 개수"),
        service: NewsQueryService = Depends(get_news_query_service),
) -> JSONResponse:
    res = service.get_news_by_keyword(query, page, size)
    return success(SuccessCode.NEWS200_1, res.model_dump())

@router.post("/collect")
def collect_news(
        service: NewsCollectService = Depends(get_news_collect_service),
) -> JSONResponse:
    res = service.collect_news()
    return success(
        SuccessCode.NEWS200_2,
        res
    )