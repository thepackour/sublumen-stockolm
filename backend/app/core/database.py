from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.schemas import Base


def get_database_url() -> str:
    return settings.DATABASE_URL


def create_db_engine(database_url: Optional[str] = None):
    url = database_url or get_database_url()

    if url.startswith("sqlite"):
        return create_engine(url)
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

    # ``create_all`` creates missing tables but does not alter tables that
    # already exist.  These columns replaced the former stock relation, so
    # add them for databases created by older versions of the application.
    if engine.dialect.name == "postgresql":
        with engine.begin() as connection:
            connection.execute(text("""
                ALTER TABLE news
                ADD COLUMN IF NOT EXISTS stock_ticker VARCHAR(100)
            """))
            connection.execute(text("""
                ALTER TABLE news
                ADD COLUMN IF NOT EXISTS stock_name VARCHAR(100)
            """))
            connection.execute(text("""
                ALTER TABLE news
                ADD COLUMN IF NOT EXISTS flag INTEGER NOT NULL DEFAULT 0
            """))
