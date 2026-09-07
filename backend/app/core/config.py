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
    KIS_BASE_URL: str = os.getenv("KIS_BASE_URL", "https://openapi.koreainvestment.com:9443")
    KIS_WEBSOCKET_URL: str = os.getenv("KIS_WEBSOCKET_URL", "ws://ops.koreainvestment.com:21000")
    KIS_APP_KEY: str = os.getenv("KIS_APP_KEY", os.getenv("KIS_APPKEY", ""))
    KIS_APP_SECRET: str = os.getenv("KIS_APP_SECRET", os.getenv("KIS_APPSECRET", ""))
    KIS_TIMEOUT_SECONDS: int = int(os.getenv("KIS_TIMEOUT_SECONDS", "10"))


settings = Settings()
