from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.technical_analysis import StrategyName


class DateRangeRequest(BaseModel):
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date는 end_date보다 늦을 수 없습니다.")
        return self


class TechnicalAnalysisRequest(DateRangeRequest):
    symbol: str = Field(min_length=1)
    strategy: StrategyName = StrategyName.SMA_CROSSOVER
    parameters: dict[str, float] = Field(default_factory=dict)
    include_history: bool = True
