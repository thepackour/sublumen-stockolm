from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
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
            stmt = (insert(News)
            .values(news)
            .on_conflict_do_nothing(
                index_elements=["url"]
            ))

            result = db.execute(stmt).fetchall()
            db.commit()
            return result

    def find_by_url(self, url: str):
        with self.session_factory() as db:
            stmt = select(News).where(News.url == url)
            return self.db.scalar(stmt)

    def find_latest_by_stock_id(self, stock_id: int, page: int = 1, size: int = 10):
        with self.session_factory() as db:
            stmt = (
                select(News)
                .where(News.stock_id == stock_id)
                .order_by(News.published_at.desc())
                .offset((page - 1) * size)
                .limit(size)
            )

            return db.scalars(stmt).all()

    def delete(self, news: News):
        with self.session_factory() as db:
            db.delete(news)
            db.commit()

    def find_all_by_ids(
            self,
            id_list: list[int],
    ):
        with self.session_factory() as db:
            stmt = (
                select(News)
                .where(News.id.in_(id_list))
            )

            return db.scalars(stmt).all()


def get_news_repository(
    db: Session = Depends(get_db),
):
    return NewsRepository(db)