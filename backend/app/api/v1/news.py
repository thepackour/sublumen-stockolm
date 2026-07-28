from fastapi import APIRouter, Query, Depends

from app.services.news_query_service import NewsQueryService


router = APIRouter(
    prefix="/api/v1/news",
    tags=["News"]
)


@router.get("")
def get_news(
        query: str = Query(..., description="검색어"),
        page: int = Query(1, description="페이지 번호"),
        size: int = Query(10, description="페이지당 뉴스 개수"),
        service: NewsQueryService = Depends(NewsQueryService),
):
    res = service.get_news_by_keyword(query, page, size)
    return {"data": res, "count": len(res)}