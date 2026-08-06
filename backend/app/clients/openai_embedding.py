from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger


class EmbeddingClient:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"


    def embed_chunks(self, chunks: list[str], show_logs: bool = True) -> list[list[float]]:
        res = self.client.embeddings.create(
            model=self.model,
            input=chunks
        )
        if show_logs: logger.info(
            "임베딩 API: 청크 %d개 생성",
            len(res.data),
        )
        return [item.embedding for item in res.data]


    def embed_keyword(self, keyword: str, show_logs: bool = True) -> list[float]:
        res = self.client.embeddings.create(
            model=self.model,
            input=keyword
        )
        if show_logs: logger.info("임베딩 API: 키워드 1개 성공")
        return res.data[0].embedding
