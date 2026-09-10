from fastapi import APIRouter, Depends, Query

from app.container import container
from app.services.exchange_rate_service import ExchangeRateService


router = APIRouter(
    prefix="/api/v1/exchange-rates",
    tags=["Exchange Rates"]
)

def get_exchange_rate_service():
    return container.exchange_rate_service


@router.get("")
def get_exchange_rates(
    query: str,
    target: str = Query(default="KRW"),
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    return service.get_exchange_rates(query, target, start_date, end_date)
