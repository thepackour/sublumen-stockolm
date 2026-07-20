from fastapi import APIRouter, Query

from app.services.exchange_rate_service import ExchangeRateService


router = APIRouter(
    prefix="/api/v1/exchange-rates",
    tags=["Exchange Rates"]
)

service = ExchangeRateService()


@router.get("")
def get_exchange_rates(
    query: str,
    target: str | None = Query(default=None)
):
    return service.get_exchange_rates(query, target)