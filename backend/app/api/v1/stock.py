from fastapi import APIRouter, Query

from app.services.stock_service import StockService

router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["Stock"]
)

service = StockService()

@router.get("")
def search_stock(
    query: str | None = Query(default=None),
    limit: int = 10
):
    return service.search_stock(query, limit)


@router.get("/{symbol}")
def get_stock(symbol: str):
    return service.get_stock(symbol)