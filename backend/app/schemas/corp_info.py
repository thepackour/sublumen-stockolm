from datetime import date
from typing import Optional

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.database import Base, TimestampMixin


class CorpInfo(Base, TimestampMixin):
    __tablename__ = "corp_infos"

    corp_code: Mapped[str] = mapped_column(String(8), nullable=False, primary_key=True)
    corp_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    corp_eng_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stock_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, index=True)
    modify_date: Mapped[date] = mapped_column(Date, nullable=False)
