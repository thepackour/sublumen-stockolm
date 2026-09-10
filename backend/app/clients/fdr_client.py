import FinanceDataReader as fdr
import pandas as pd
from pandas import DataFrame
from FinanceDataReader.krx.listing import KrxStockListing

from app.core.logger import logger
from app.dto.StockInfo import StockInfo


class FdrClient:

    def get_stock_list(self) -> list[StockInfo]:
        listings = []
        krx = self._get_krx_listing()
        if not krx.empty:
            listings.append(self._normalize_listing(krx, "KRX"))

        nasdaq = self._get_listing("NASDAQ")
        if not nasdaq.empty:
            listings.append(self._normalize_listing(nasdaq, "NASDAQ"))

        if not listings:
            raise RuntimeError("종목 목록을 제공하는 외부 서비스를 사용할 수 없습니다.")

        catalog = pd.concat(listings, ignore_index=True)
        domestic_markets = {
            "KRX", "KOSPI", "KOSDAQ", "KOSDAQ GLOBAL", "KONEX"
        }

        return [
            StockInfo(
                symbol=str(row.Symbol),
                name=str(row.Name),
                market=str(row.Market),
                sector=None if pd.isna(row.Sector) else row.Sector,
                industry=None if pd.isna(row.Industry) else row.Industry,
                is_domestic=row.Market in domestic_markets,
                currency="KRW" if row.Market in domestic_markets else "USD",
            )
            for row in catalog.itertuples()
            if not pd.isna(row.Market)
        ]

    @staticmethod
    def _get_listing(market: str, log_exception: bool = True) -> DataFrame:
        try:
            return fdr.StockListing(market)
        except Exception as exc:
            if log_exception:
                logger.exception("FinanceDataReader 종목 목록 조회 실패 (%s)", market)
            else:
                logger.warning(
                    "FinanceDataReader 캐시 종목 목록 조회 실패 (%s): %s",
                    market,
                    exc,
                )
            return DataFrame()

    def _get_krx_listing(self) -> DataFrame:
        cached = self._get_listing("KRX-DESC", log_exception=False)
        if not cached.empty:
            return cached

        logger.warning("KRX 캐시 목록을 사용할 수 없어 원본 목록 조회로 전환합니다.")
        try:
            return KrxStockListing("KRX-DESC").read()
        except Exception:
            logger.exception("KRX 원본 종목 목록 조회 실패")
            return DataFrame()

    @staticmethod
    def _normalize_listing(listing: DataFrame, default_market: str) -> DataFrame:
        normalized = listing.rename(columns={"Code": "Symbol"}).copy()
        if "Market" not in normalized:
            normalized["Market"] = default_market
        if "Sector" not in normalized:
            normalized["Sector"] = None
        if "Industry" not in normalized:
            normalized["Industry"] = None
        return normalized[["Symbol", "Name", "Market", "Sector", "Industry"]]

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
