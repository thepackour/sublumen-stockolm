from datetime import datetime

from pydantic import BaseModel


class NewsResponse(BaseModel):
    news_id: int
    title: str
    summary: str
    source: str
    url: str
    published_at: datetime

    related_stock_id: int
    related_stock_name: str