from fastapi import APIRouter, Query

from app.services.news_service import NewsService


router = APIRouter(
    prefix="/api/v1/news",
    tags=["News"]
)

service = NewsService()


@router.get("")
def get_news(
    query: str = Query(..., description="검색어"),
    stock: str = Query(None, description="종목 코드"),
    page: int = Query(1, description="페이지 번호"),
    size: int = Query(10, description="페이지당 뉴스 개수")
):
    res = service.get_news(query=query, stock=stock, page=page, size=size)
    return {"data": res, "count": len(res)}