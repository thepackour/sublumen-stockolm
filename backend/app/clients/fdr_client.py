import FinanceDataReader as fdr
import pandas as pd
from pandas import DataFrame

from app.dto.StockInfo import StockInfo


class FdrClient:

    def get_stock_list(self) -> list[StockInfo]:
        krx = fdr.StockListing("KRX-DESC").rename(columns={"Code": "Symbol"})
        nasdaq = fdr.StockListing("NASDAQ")

        return [
            StockInfo(
                symbol=row.Symbol,
                name=row.Name,
                market=row.Market,
                sector=None if pd.isna(row.Sector) else row.Sector,
                industry=None if pd.isna(row.Industry) else row.Industry,
                # is_domestic=row.Market in ["KRX"],
                # currency=None if pd.isna(row.Market) else market_currency_table.get(row.Market)
            )
            for row in pd.concat([krx, nasdaq], ignore_index=True).itertuples()
            if not pd.isna(row.Market)
        ]

    def get_stock_price(
            self,
            symbol: str,
            start: str,
            end: str | None = None,
    ) -> DataFrame:
        """

        Args:
            symbol: 주식 심볼(ticker)
            start: 시작 일자
            end: 끝 일자

        Returns: DataFrame (!!!)

        """
        return fdr.DataReader(symbol, start, end)

    def get_today_stock_price(self, symbol: str) -> DataFrame:
        return self.get_stock_price(symbol, "TODAY", "TODAY")