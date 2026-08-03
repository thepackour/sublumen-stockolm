from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.database import Base, TimestampMixin


class Stock(Base, TimestampMixin):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    market: Mapped[str] = mapped_column(String(50), nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_domestic: Mapped[bool] = mapped_column(Boolean, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=True)

    financial_statements: Mapped[list["FinancialStatement"]] = relationship(
        "FinancialStatement", back_populates="stock", cascade="all, delete-orphan"
    )
    news_items: Mapped[list["News"]] = relationship(
        "News", back_populates="stock", cascade="all, delete-orphan"
    )
    analyses: Mapped[list["Analysis"]] = relationship(
        "Analysis", back_populates="stock", cascade="all, delete-orphan"
    )
    backtests: Mapped[list["Backtest"]] = relationship(
        "Backtest", back_populates="stock", cascade="all, delete-orphan"
    )
    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(
        "PortfolioItem", back_populates="stock", cascade="all, delete-orphan"
    )
