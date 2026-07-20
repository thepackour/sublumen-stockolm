from app.repositories.mock_stock_repository import StockRepository
from app.schemas.backtest import BacktestCreateRequest
from app.core.exceptions import ProjectException
from app.core.error_code import ErrorCode

stock_repository = StockRepository()


class BacktestService:

    def __init__(self):
        self.backtest_store: dict[str, dict] = {}

    def create_backtest(self, request: BacktestCreateRequest):
        backtest_id = f"backtest-{len(self.backtest_store) + 1}"
        detail = stock_repository.get_stock_detail(request.symbol)
        self.backtest_store[backtest_id] = {
            "backtestId": backtest_id,
            "symbol": detail["symbol"],
            "strategy": request.strategy,
            "initialCapital": request.initial_capital,
            "finalValue": round(request.initial_capital * 1.18, 2),
            "returnRate": 18.0,
            "sharpeRatio": 1.24,
        }
        return self.backtest_store[backtest_id]


    def get_backtest(self, backtest_id: str):
        if backtest_id not in self.backtest_store:
            raise ProjectException(ErrorCode.BACKTEST404_1)
        return self.backtest_store[backtest_id]
