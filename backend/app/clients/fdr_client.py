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
                symbol=str(row.Symbol),
                name=str(row.Name),
                market=str(row.Market),
                sector=None if pd.isna(row.Sector) else row.Sector,
                industry=None if pd.isna(row.Industry) else row.Industry,
                is_domestic=row.Market in {
                    "KRX", "KOSPI", "KOSDAQ", "KOSDAQ GLOBAL", "KONEX"
                },
                currency="KRW" if row.Market in {
                    "KRX", "KOSPI", "KOSDAQ", "KOSDAQ GLOBAL", "KONEX"
                } else "USD",
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

    def get_exchange_rate(
            self,
            base_currency: str,
            target_currency: str,
            start: str,
            end: str | None = None,
    ) -> DataFrame:
        """Fetch an exchange-rate series without persisting it."""
        symbol = (
            f"YAHOO:{base_currency.upper()}"
            f"{target_currency.upper()}=X"
        )
        return fdr.DataReader(symbol, start, end)
