from __future__ import annotations

from datetime import datetime
from typing import Optional

from pgvector import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas import News
from app.schemas.database import Base, TimestampMixin


class NewsEmbedding(Base, TimestampMixin):
    __tablename__ = "news_embedding"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    stock_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stocks.id"), nullable=True)
    chunk_index: Mapped[int]
    chunk_text: Mapped[str]
    embedding: Mapped[Vector]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    news: Mapped[Optional["News"]] = relationship(back_populates="embeddings")
