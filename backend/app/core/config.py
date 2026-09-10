import os
from dotenv import load_dotenv

if os.getenv("ENV") != "docker":
    load_dotenv("dev.env")


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv(
        "DB_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/stockolm",
    )
    NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID", "")
    NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET", "")
    DART_API_KEY: str = os.getenv("DART_API_KEY", "")
    DART_BASE_URL: str = os.getenv(
        "DART_BASE_URL",
        "https://opendart.fss.or.kr/api",
    )
    DART_TIMEOUT_SECONDS: float = float(os.getenv("DART_TIMEOUT_SECONDS", "10"))
    STOCK_CATALOG_CACHE_TTL_SECONDS: int = int(
        os.getenv("STOCK_CATALOG_CACHE_TTL_SECONDS", "86400")
    )


settings = Settings()
