from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.news import News
from app.core.database import get_db


class NewsRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, news: News):
        with self.session_factory() as db:
            db.add(news)
            db.commit()
            db.refresh(news)
            return news

    def save_all(self, news: list[News]):
        with self.session_factory() as db:
            db.add_all(news)
            db.commit()
            db.refresh(news)
            return news

    def find_by_url(self, url: str):
        with self.session_factory() as db:
            stmt = select(News).where(News.url == url)
            return db.scalar(stmt)

    def find_latest(self, stock_id: int, limit: int = 10):
        with self.session_factory() as db:
            stmt = (
                select(News)
                .where(News.stock_id == stock_id)
                .order_by(News.published_at.desc())
                .limit(limit)
            )

            return db.scalars(stmt).all()

    def find_all(self):
        with self.session_factory() as db:
            stmt = select(News)

            return db.scalars(stmt).all()


def get_news_repository(
    db: Session = Depends(get_db),
):
    return NewsRepository(db)