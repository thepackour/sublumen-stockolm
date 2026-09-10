from datetime import datetime, timedelta

from pandas import isna

from app.clients.fdr_client import FdrClient
from app.core.error_code import ErrorCode
from app.core.exceptions import ProjectException


class ExchangeRateService:

    def __init__(self, fdr_client: FdrClient):
        self.fdr_client = fdr_client

    def get_exchange_rates(
            self,
            base_currency: str,
            target_currency: str = "KRW",
            start_date: str | None = None,
            end_date: str | None = None,
    ) -> list[dict]:
        base = base_currency.upper()
        target = target_currency.upper()

        if base == target:
            return [{
                "base_currency": base,
                "target_currency": target,
                "rate": 1.0,
                "date": datetime.now().date().isoformat(),
            }]

        latest_only = start_date is None and end_date is None
        start = start_date or (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        try:
            data = self.fdr_client.get_exchange_rate(base, target, start, end_date)
        except Exception as exc:
            raise ProjectException(ErrorCode.EXCHANGERATE404_1) from exc

        if data.empty:
            raise ProjectException(ErrorCode.EXCHANGERATE404_1)

        records = [
            {
                "base_currency": base,
                "target_currency": target,
                "rate": float(row["Close"]),
                "date": index.date().isoformat() if hasattr(index, "date") else str(index),
            }
            for index, row in data.iterrows()
            if not isna(row["Close"])
        ]
        if not records:
            raise ProjectException(ErrorCode.EXCHANGERATE404_1)
        return records[-1:] if latest_only else records
