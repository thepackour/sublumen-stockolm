from __future__ import annotations

from pydantic import Field

from app.schemas.technical_analysis import DateRangeRequest
from app.technical_analysis import StrategyName


class BacktestCreateRequest(DateRangeRequest):
    symbol: str = Field(min_length=1)
    strategy: StrategyName = StrategyName.SMA_CROSSOVER
    parameters: dict[str, float] = Field(default_factory=dict)
    initial_capital: float = Field(default=1_000_000.0, gt=0)
    commission_rate: float = Field(default=0.00015, ge=0, lt=1)
    slippage_rate: float = Field(default=0.0005, ge=0, lt=1)
