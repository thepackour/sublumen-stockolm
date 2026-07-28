from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.schemas.news import News
from app.core.database import get_db


class NewsRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, news: News):
        self.db.add(news)
        self.db.commit()
        self.db.refresh(news)
        return news

    def save_all(self, news: list[News]):
        stmt = (insert(News)
        .values(news)
        .on_conflict_do_nothing(
            index_elements=["url"]
        ))

        result = self.db.execute(stmt).fetchall()
        self.db.commit()
        return result

    def find_by_url(self, url: str):
        stmt = select(News).where(News.url == url)
        return self.db.scalar(stmt)

    def find_latest(self, stock_id: int, limit: int = 10):
        stmt = (
            select(News)
            .where(News.stock_id == stock_id)
            .order_by(News.published_at.desc())
            .limit(limit)
        )

        return self.db.scalars(stmt).all()

    def find_all(self):
        stmt = select(News)

        return self.db.scalars(stmt).all()

    def delete(self, news: News):
        self.db.delete(news)
        self.db.commit()


def get_news_repository(
    db: Session = Depends(get_db),
):
    return NewsRepository(db)