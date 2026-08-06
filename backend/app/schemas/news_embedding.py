from __future__ import annotations

from datetime import datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.database import Base, TimestampMixin


class NewsEmbedding(Base, TimestampMixin):

    __tablename__ = "news_embedding"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    news_id: Mapped[int] = mapped_column(
        ForeignKey("news.id"),
        nullable=False,
        index=True
    )

    stock_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stocks.id"),
        nullable=True,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    chunk_text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=False
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    news: Mapped["News"] = relationship(
        "News",
        back_populates="embeddings"
    )