from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.database import Base, TimestampMixin


class News(Base, TimestampMixin):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stocks.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    stock: Mapped[Optional["Stock"]] = relationship("Stock", back_populates="news_items")
    embeddings: Mapped[Optional["NewsEmbeddings"]] = relationship("NewsEmbeddings", back_populates="news")
