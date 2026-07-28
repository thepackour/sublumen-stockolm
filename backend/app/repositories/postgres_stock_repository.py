from datetime import datetime

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.stock import Stock
from app.core.database import get_db


class StockRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, stock: Stock):
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def save_all(self, stocks: list[Stock]):
        self.db.add_all(stocks)
        self.db.commit()
        self.db.refresh(stocks)
        return stocks

        return self.db.scalars(stmt).all()

    def find_all(self):
        stmt = select(Stock)

        return self.db.scalars(stmt).all()

    def delete(self, stock: Stock, hard_delete: bool | None = False):
        if hard_delete:
            self.db.delete(stock)
            self.db.commit()
        else:
            stmt = select(Stock).where(Stock.id == stock.id)
            res = self.db.execute(stmt)
            res.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(stock)


def get_stock_repository(
    db: Session = Depends(get_db),
):
    return StockRepository(db)