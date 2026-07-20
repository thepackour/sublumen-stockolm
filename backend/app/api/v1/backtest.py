from fastapi import APIRouter

from app.schemas.backtest import BacktestCreateRequest
from app.services.backtest_service import BacktestService

router = APIRouter(
    prefix="/api/v1/backtests",
    tags=["Backtests"]
)

service = BacktestService()


@router.post("")
def create_backtest(request: BacktestCreateRequest):
    return service.create_backtest(request)


@router.get("/{backtest_id}")
def get_backtest(backtest_id: str):
    return service.get_backtest(backtest_id)