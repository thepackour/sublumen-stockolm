from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.database import Base, TimestampMixin


class FinancialStatement(Base, TimestampMixin):
    __tablename__ = "financial_statements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)

    business_year: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)

    fs_div: Mapped[str] = mapped_column(String(3), nullable=False)
    fs_name: Mapped[str] = mapped_column(String(50), nullable=False)

    receipt_no: Mapped[str] = mapped_column(String(20), nullable=False)
    
    items = relationship(
        "FinancialStatementItem",
        back_populates="statement",
        cascade="all, delete-orphan",
    )
    stock: Mapped["Stock"] = relationship(
        "Stock",
        back_populates="financial_statements"
    )

    __table_args__ = (
        UniqueConstraint(
            "receipt_no",
            "fs_div",
            name="uq_financial_statement_receipt_fs_div"
        ),
    )