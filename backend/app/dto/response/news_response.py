from pydantic import BaseModel


class NewsResponse(BaseModel):
    news_id: int
    title: str
    summary: str
    source: str
    url: str
    published_at: str

    related_stock_id: str
    related_stock_name: str