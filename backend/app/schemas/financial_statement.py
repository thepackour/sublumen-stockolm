from __future__ import annotations

from typing import Optional

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.database import Base, TimestampMixin


class FinancialStatement(Base, TimestampMixin):
    __tablename__ = "financial_statements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    corp_code: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
    corp_name: Mapped[str] = mapped_column(String(255), nullable=False)
    stock_ticker: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    net_income: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    eps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    debt_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
