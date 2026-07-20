import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.schemas.database import Base


def get_database_url() -> str:
    return settings.DATABASE_URL or "postgresql+psycopg2://postgres:postgres@localhost:5432/sublumen_stockolm"


def create_db_engine(database_url: Optional[str] = None):
    url = database_url or get_database_url()
    if url.startswith("sqlite"):
        return create_engine(url)

    return create_engine(url, pool_pre_ping=True)


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
