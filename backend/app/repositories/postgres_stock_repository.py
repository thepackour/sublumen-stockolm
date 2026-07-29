from datetime import datetime
from typing import Optional

from sqlalchemy import select

from app.schemas.stock import Stock


class StockRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, stock: Stock):
        with self.session_factory() as db:
            db.add(stock)
            db.commit()
            db.refresh(stock)
            return stock

    def save_all(self, stocks: list[Stock]):
        with self.session_factory() as db:
            db.add_all(stocks)
            db.commit()
            db.refresh(stocks)
            return stocks

    def find_all(self):
        stmt = select(Stock)
        with self.session_factory() as db:
            return db.scalars(stmt).all()

    def find_by_symbol(self, symbol: str) -> Optional[Stock]:
        with self.session_factory() as db:
            stmt = (
                select(Stock)
                .where(Stock.symbol == symbol)
            )
            return db.scalars(stmt).one()

    def delete(self, stock: Stock, hard_delete: bool | None = False):
        with self.session_factory() as db:
            if hard_delete:
                db.delete(stock)
                db.commit()
            else:
                stmt = select(Stock).where(Stock.id == stock.id)
                res = db.execute(stmt)
                res.deleted_at = datetime.now()
                db.commit()
                db.refresh(stock)