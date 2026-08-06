from google import genai
from google.genai import types

from app.core.config import settings
from app.core.logger import logger


class EmbeddingClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )
        self.model = self.client.models

    def embed_chunks(self, chunks: list[str], show_logs: bool = True) -> list[list[float]]:
        res = self.model.embed_content(
            model="gemini-embedding-2",
            contents=[
                types.Content(
                    parts=[types.Part.from_text(text=c)]
                )
                for c in chunks
            ]
        )
        if show_logs: logger.info(
            "임베딩 API: 청크 %d개 생성",
            len(res.embeddings),
        )
        return [embedding.value for embedding in res.embeddings]

    def embed_keyword(self, keyword: str, show_logs: bool = True) -> list[float]:
        res = self.model.embed_content(
            model="gemini-embedding-2",
            contents=[
                types.Content(
                    parts=[types.Part.from_text(text=keyword)]
                )
            ]
        )
        if show_logs: logger.info("임베딩 API: 키워드 1개 성공")
        return res.embeddings[0].values