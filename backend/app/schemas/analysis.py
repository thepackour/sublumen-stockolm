from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from app.schemas.database import Base, TimestampMixin


class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    result_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    stock: Mapped["Stock"] = relationship("Stock", back_populates="analyses")


class AnalysisCreateRequest(BaseModel):
    symbol: str
    analysis_type: str = "summary"
