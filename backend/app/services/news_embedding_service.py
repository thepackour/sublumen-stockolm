from app.clients.openai_embedding import EmbeddingClient
from app.schemas import News
from app.schemas.news_embedding import NewsEmbedding
from app.util.news_chunker import NewsChunker


class NewsEmbeddingService:

    def __init__(
            self,
            embedding_client: EmbeddingClient,
    ):
        self.embedding_client = embedding_client
        self.news_chunker = NewsChunker()

    def embed_news(self, news: News) -> list[NewsEmbedding]:
        text = f"""\
        제목: {news.title}
        {news.content}"""

        chunks = self.news_chunker.split(text)
        embeddings = self.embedding_client.embed_chunks(chunks, False)
        return [
            NewsEmbedding(
                news_id=news.id,
                stock_id=news.stock_id,
                chunk_index=i,
                chunk_text=chunks[i],
                embedding=embeddings[i],
                published_at=news.published_at,
            )
            for i in range(len(embeddings))
        ]
