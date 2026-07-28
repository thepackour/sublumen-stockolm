from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas import TimestampMixin
from app.schemas.database import Base


class NewsKeyword(Base, TimestampMixin):
    __tablename__ = "news_keyword"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    next_collect_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)