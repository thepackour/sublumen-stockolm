import json

from fastapi import APIRouter, Query, Depends
from fastapi.responses import StreamingResponse

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
    if not query:
        return []
    return [service.get_stock(query)]


@router.get("/{symbol}")
def get_stock(
        symbol: str,
        service: StockQueryService = Depends(get_stock_query_service),
):
    return service.get_stock(symbol)

@router.get("/{symbol}/history")
def get_stock_history(symbol: str, start: str | None = None, end: str | None = None, service: StockQueryService = Depends(get_stock_query_service)):
    return service.get_stock_history(symbol, start, end)

@router.get("/{symbol}/price")
def get_stock_price(symbol: str, service: StockQueryService = Depends(get_stock_query_service)):
    return service.get_stock_price_for_agent(symbol)

@router.get("/{symbol}/financial")
def get_financial(symbol: str, service: StockQueryService = Depends(get_stock_query_service)):
    return service.get_financial(symbol)

@router.get("/{symbol}/stream")
async def stream_stock(symbol: str, service: StockQueryService = Depends(get_stock_query_service)):
    resolved = service.resolve(symbol)

    async def events():
        async for tick in service.realtime_client.stream(resolved):
            yield f"event: tick\ndata: {json.dumps(tick, ensure_ascii=False)}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive"})
