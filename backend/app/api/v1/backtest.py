from fastapi import APIRouter, Depends

from app.container import container
from app.schemas.backtest import BacktestCreateRequest
from app.services.backtest_service import BacktestService

router = APIRouter(
    prefix="/api/v1/backtests",
    tags=["Backtests"]
)

def get_backtest_service() -> BacktestService:
    return container.backtest_service


@router.post("")
def create_backtest(
    request: BacktestCreateRequest,
    service: BacktestService = Depends(get_backtest_service),
):
    return service.create_backtest(request)
