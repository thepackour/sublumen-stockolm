from fastapi import Depends
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from app.schemas.news_embedding import NewsEmbedding
from app.core.database import get_db


class NewsEmbeddingRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_all(self, embeddings: list[NewsEmbedding]) -> None:
        self.db.add_all(embeddings)
        self.db.commit()

    def similarity_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[NewsEmbedding]:
        stmt = (
            select(NewsEmbedding)
            .order_by(
                NewsEmbedding.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        return list(self.db.scalars(stmt))

    def search_news_id_by_embedding(
            self,
            query_embedding: list[float],
            page: int = 1,
            limit: int = 5,
    ) -> tuple[list[tuple[int, float]], int]:
        distance = NewsEmbedding.embedding.cosine_distance(query_embedding)

        # 데이터 조회
        stmt = (
            select(
                NewsEmbedding.news_id,
                func.min(distance).label("score"),
            )
            .group_by(NewsEmbedding.news_id)
            .order_by("score")
            .offset((page - 1) * limit)
            .limit(limit)
        )

        items = self.db.execute(stmt).all()

        # 전체 개수 조회
        count_stmt = (
            select(func.count())
            .select_from(
                select(NewsEmbedding.news_id)
                .group_by(NewsEmbedding.news_id)
                .subquery()
            )
        )

        total_count = self.db.scalar(count_stmt)

        return items, total_count

    def delete_by_news_id(
            self,
            news_id: int,
    ) -> None:

        self.db.execute(
            delete(NewsEmbedding)
            .where(NewsEmbedding.news_id == news_id)
        )

        self.db.commit()


def get_news_embedding_repository(
    db: Session = Depends(get_db),
):
    return NewsEmbeddingRepository(db)