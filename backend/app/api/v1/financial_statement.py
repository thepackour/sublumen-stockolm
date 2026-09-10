from fastapi import APIRouter, Depends, Query

from app.container import container
from app.services.stock_query_service import StockQueryService

router = APIRouter(prefix="/api/v1/financial-statement", tags=["Financial"])


def get_stock_query_service():
    return container.stock_query_service


@router.get("")
def get_financial_statement(
    query: str = Query(..., description="국내주식 6자리 종목코드"),
    service: StockQueryService = Depends(get_stock_query_service),
):
    return service.get_financial(query)
