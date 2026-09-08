from sqlalchemy import select

from app.schemas.news import News


class NewsRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def find_by_url(self, url: str):
        with self.session_factory() as db:
            stmt = select(News).where(News.url == url)
            return db.scalar(stmt)

    def find_latest(self, stock_ticker: str, limit: int = 10):
        with self.session_factory() as db:
            stmt = (
                select(News)
                .where(News.stock_ticker == stock_ticker)
                .order_by(News.published_at.desc())
                .limit(limit)
            )

            return db.scalars(stmt).all()

    def find_all(self):
        with self.session_factory() as db:
            stmt = select(News)

            return db.scalars(stmt).all()
