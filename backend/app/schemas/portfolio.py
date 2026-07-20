from __future__ import annotations

from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.database import Base, TimestampMixin


class Portfolio(Base, TimestampMixin):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expected_return: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="portfolios")
    items: Mapped[list["PortfolioItem"]] = relationship(
        "PortfolioItem", back_populates="portfolio", cascade="all, delete-orphan"
    )


class PortfolioItem(Base, TimestampMixin):
    __tablename__ = "portfolio_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    buy_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="items")
    stock: Mapped["Stock"] = relationship("Stock", back_populates="portfolio_items")
