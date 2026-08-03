from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.schemas import Base


def get_database_url() -> str:
    return settings.DATABASE_URL


def create_db_engine(database_url: Optional[str] = None):
    url = database_url or get_database_url()

    if url.startswith("sqlite"):
        return create_engine(url)
    print("db url: " + url)
    return create_engine(
        url,
        pool_pre_ping=True,
    )


engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)