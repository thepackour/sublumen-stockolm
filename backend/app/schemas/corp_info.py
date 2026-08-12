from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas import TimestampMixin, Base


class CorpInfo(Base, TimestampMixin):
    __tablename__ = "corp_infos"

    corp_code: Mapped[str] = mapped_column(String(8), nullable=False, primary_key=True)
    corp_name: Mapped[str] = mapped_column(String(50), nullable=False)
    corp_eng_name: Mapped[str] = mapped_column(String(50), nullable=False)
    stock_code: Mapped[str] = mapped_column(String(6), nullable=False)
    modify_date: Mapped[TimestampMixin] = mapped_column()