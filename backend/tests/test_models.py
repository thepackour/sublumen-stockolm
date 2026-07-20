import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.database import Base
from app.schemas.user import User


def test_create_tables_and_insert_user():
    database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/sublumen_stockolm")
    if database_url.startswith("postgresql"):
        try:
            engine = create_engine(database_url)
            with engine.connect() as connection:
                connection.execute("SELECT 1")
        except Exception:
            engine = create_engine("sqlite:///:memory:")
    else:
        engine = create_engine(database_url)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        user = User(
            name="Alice",
            email="alice@example.com",
            password_hash="hash",
            role="user",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.deleted_at is None
