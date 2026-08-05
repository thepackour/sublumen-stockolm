import os
from dotenv import load_dotenv

if os.getenv("ENV") != "docker":
    load_dotenv("dev.env")


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPEN_API_KEY: str = os.getenv("OPEN_API_KEY", "")
    DATABASE_URL: str = os.getenv(
        "DB_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/stockolm",
    )
    NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID", "")
    NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET", "")
    DART_API_KEY: str = os.getenv("DART_API_KEY", "")


settings = Settings()