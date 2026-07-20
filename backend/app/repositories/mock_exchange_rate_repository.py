from datetime import datetime, timezone, timedelta

# 기준 시간 설정 (최근 일자)
base_date = datetime(2026, 7, 20, 15, 0, 0, tzinfo=timezone.utc)

__EXCHANGE_RATE_SAMPLES = [
    {
        "id": 1,
        "base_currency": "USD",
        "target_currency": "KRW",
        "rate": 1382.50,
        "date": base_date
    },
    {
        "id": 2,
        "base_currency": "USD",
        "target_currency": "KRW",
        "rate": 1378.20,
        "date": base_date - timedelta(days=1)
    },
    {
        "id": 3,
        "base_currency": "USD",
        "target_currency": "KRW",
        "rate": 1374.00,
        "date": base_date - timedelta(days=2)
    },
    {
        "id": 4,
        "base_currency": "USD",
        "target_currency": "KRW",
        "rate": 1379.10,
        "date": base_date - timedelta(days=3)
    },
    {
        "id": 5,
        "base_currency": "USD",
        "target_currency": "KRW",
        "rate": 1385.40,
        "date": base_date - timedelta(days=4)
    },
    {
        "id": 6,
        "base_currency": "EUR",
        "target_currency": "KRW",
        "rate": 1502.10,
        "date": base_date
    },
    {
        "id": 7,
        "base_currency": "EUR",
        "target_currency": "KRW",
        "rate": 1498.50,
        "date": base_date - timedelta(days=1)
    },
    {
        "id": 8,
        "base_currency": "EUR",
        "target_currency": "KRW",
        "rate": 1495.30,
        "date": base_date - timedelta(days=2)
    },
    {
        "id": 9,
        "base_currency": "JPY",
        "target_currency": "KRW",
        "rate": 8.75,  # 1엔당 원화 비율 (보통 100엔당 875원 형태이나 단일 통화 기준)
        "date": base_date
    },
    {
        "id": 10,
        "base_currency": "JPY",
        "target_currency": "KRW",
        "rate": 8.72,
        "date": base_date - timedelta(days=1)
    },
    {
        "id": 11,
        "base_currency": "JPY",
        "target_currency": "KRW",
        "rate": 8.68,
        "date": base_date - timedelta(days=2)
    },
    {
        "id": 12,
        "base_currency": "EUR",
        "target_currency": "USD",
        "rate": 1.0865,
        "date": base_date
    },
    {
        "id": 13,
        "base_currency": "EUR",
        "target_currency": "USD",
        "rate": 1.0872,
        "date": base_date - timedelta(days=1)
    },
    {
        "id": 14,
        "base_currency": "EUR",
        "target_currency": "USD",
        "rate": 1.0883,
        "date": base_date - timedelta(days=2)
    },
    {
        "id": 15,
        "base_currency": "USD",
        "target_currency": "JPY",
        "rate": 158.00,
        "date": base_date
    },
    {
        "id": 16,
        "base_currency": "USD",
        "target_currency": "JPY",
        "rate": 158.08,
        "date": base_date - timedelta(days=1)
    },
    {
        "id": 17,
        "base_currency": "USD",
        "target_currency": "JPY",
        "rate": 158.30,
        "date": base_date - timedelta(days=2)
    },
    {
        "id": 18,
        "base_currency": "GBP",
        "target_currency": "KRW",
        "rate": 1785.40,
        "date": base_date
    },
    {
        "id": 19,
        "base_currency": "AUD",
        "target_currency": "KRW",
        "rate": 921.20,
        "date": base_date
    },
    {
        "id": 20,
        "base_currency": "CNY",
        "target_currency": "KRW",
        "rate": 190.15,
        "date": base_date
    }
]


class ExchangeRateRepository:

    def get_exchange_rates(self, base_currency, target_currency):
        # pair = f"{base_currency}/{target_currency}"
        for rate in __EXCHANGE_RATE_SAMPLES:
            if rate["base_currency"] == base_currency and rate["target_currency"] == target_currency:
                return [rate]
        return __EXCHANGE_RATE_SAMPLES
    
    def search_exchange_rates_by_base_currency(self, base_currency, page: int = 1, size: int = 10):
        rate = [rate for rate in __EXCHANGE_RATE_SAMPLES if rate["base_currency"] == base_currency]
        return rate[(page - 1) * size: page * size] if size is not None else rate
