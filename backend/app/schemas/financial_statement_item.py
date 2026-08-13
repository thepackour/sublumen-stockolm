from datetime import date

from sqlalchemy import Integer, ForeignKey, String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas import Base, TimestampMixin


class FinancialStatementItem(Base, TimestampMixin):
    __tablename__ = "financial_statement_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)

    statement_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("financial_statements.id"),
        nullable=False
    )

    # BS / IS / CF 등
    statement_type: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    account_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    order: Mapped[Integer] = mapped_column(
        Integer,
        nullable=False
    )

    current_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    current_period_start: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    current_period_end: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )

    previous_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    previous_period_start: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    previous_period_end: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=True
    )

    statement = relationship(
        "FinancialStatement",
        back_populates="items"
    )

    __table_args__ = (
        UniqueConstraint(
            "statement_id",
            "statement_type",
            "account_name",
            "order",
            name="uq_financial_statement_item"
        )
    )