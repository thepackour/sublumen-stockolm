from fastapi import APIRouter, Query, Depends

from app.container import container
from app.services.stock_query_service import StockQueryService

router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["Stock"]
)

@router.get("")
def search_stock(
    query: str | None = Query(default=None),
    limit: int = 10,
    service: StockQueryService = Depends(StockQueryService),
):
    return service.search_stock(query, limit)


@router.get("/{symbol}")
def get_stock(
        symbol: str,
        service: StockQueryService = Depends(StockQueryService),
):
    return service.get_stock(symbol)


def get_stock_query_service() -> StockQueryService:
    return container.stock_query_service