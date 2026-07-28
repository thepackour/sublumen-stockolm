from langchain_google_genai import GoogleGenerativeAIEmbeddings


class GeminiEmbeddingClient:

    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    def embed_query(self, text: str) -> list[float]:
        return self.model.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.embed_documents(texts)