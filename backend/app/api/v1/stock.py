from fastapi import APIRouter, Query, Depends

from app.container import container
from app.services.stock_query_service import StockQueryService

router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["Stock"]
)

def get_stock_query_service():
    return container.stock_query_service

@router.get("")
def search_stock(
    query: str | None = Query(default=None),
    limit: int = 10,
    service: StockQueryService = Depends(get_stock_query_service),
):
    return service.search_stock(query, limit)


@router.get("/{symbol}")
def get_stock(
        symbol: str,
        service: StockQueryService = Depends(get_stock_query_service),
):
    return service.get_stock(symbol)