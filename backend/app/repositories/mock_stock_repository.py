__SAMPLE_STOCKS = [
    {
        "id": 1,
        "symbol": "005930",
        "name": "삼성전자",
        "market": "KOSPI",
        "sector": "반도체 및 반도체 장비",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 2,
        "symbol": "005380",
        "name": "현대자동차",
        "market": "KOSPI",
        "sector": "자동차 및 부품",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 3,
        "symbol": "035420",
        "name": "NAVER",
        "market": "KOSPI",
        "sector": "양방향 미디어 및 서비스",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 4,
        "symbol": "373220",
        "name": "LG에너지솔루션",
        "market": "KOSPI",
        "sector": "전기장비",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 5,
        "symbol": "068270",
        "name": "셀트리온",
        "market": "KOSPI",
        "sector": "제약 및 바이오테크놀로지",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 6,
        "symbol": "035720",
        "name": "카카오",
        "market": "KOSPI",
        "sector": "양방향 미디어 및 서비스",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 7,
        "symbol": "005490",
        "name": "POSCO홀딩스",
        "market": "KOSPI",
        "sector": "철강 및 금속",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 8,
        "symbol": "055550",
        "name": "신한지주",
        "market": "KOSPI",
        "sector": "은행",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 9,
        "symbol": "000660",
        "name": "SK하이닉스",
        "market": "KOSPI",
        "sector": "반도체 및 반도체 장비",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 10,
        "symbol": "139480",
        "name": "이마트",
        "market": "KOSPI",
        "sector": "소매유통",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 11,
        "symbol": "000880",
        "name": "한화에어로스페이스",
        "market": "KOSPI",
        "sector": "우주항공 및 국방",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 12,
        "symbol": "247540",
        "name": "에코프로비엠",
        "market": "KOSDAQ",
        "sector": "화학 (이차전지 소재)",
        "is_domestic": True,
        "currency": "KRW"
    },
    {
        "id": 13,
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "market": "NASDAQ",
        "sector": "기술 하드웨어, 스토리지 및 주변기기",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 14,
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "market": "NASDAQ",
        "sector": "소프트웨어",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 15,
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "market": "NASDAQ",
        "sector": "반도체 및 반도체 장비",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 16,
        "symbol": "TSLA",
        "name": "Tesla, Inc.",
        "market": "NASDAQ",
        "sector": "자동차",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 17,
        "symbol": "AMZN",
        "name": "Amazon.com, Inc.",
        "market": "NASDAQ",
        "sector": "대형 소매유통",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 18,
        "symbol": "KO",
        "name": "The Coca-Cola Company",
        "market": "NYSE",
        "sector": "음료",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 19,
        "symbol": "O",
        "name": "Realty Income Corporation",
        "market": "NYSE",
        "sector": "리츠(REITs)",
        "is_domestic": False,
        "currency": "USD"
    },
    {
        "id": 20,
        "symbol": "012330",
        "name": "현대모비스",
        "market": "KOSPI",
        "sector": "자동차 부품",
        "is_domestic": True,
        "currency": "KRW"
    }
]

class StockRepository:

    def search(self, keyword, limit):
        ...

    def find(self, symbol) -> dict:
        normalized = symbol.upper()
        for stock in __SAMPLE_STOCKS:
            if stock["symbol"] == normalized:
                return {
                    **stock,
                    "price": 98000 if normalized == "005930" else 62000 if normalized == "000660" else 215.4 if normalized == "AAPL" else 420.7,
                    "volume": 12800000,
                    "change_percent": 1.42,
                }
        return {
            "symbol": normalized,
            "name": f"{normalized} 종목",
            "market": "KRX",
            "sector": "기타",
            "currency": "KRW",
            "price": 100000,
            "volume": 5000000,
            "change_percent": 0.0,
        }