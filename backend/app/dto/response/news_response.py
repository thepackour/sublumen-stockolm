from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsResponse(BaseModel):
    news_id: int
    title: str
    summary: Optional[str]
    url: str
    published_at: datetime

    related_stock_ticker: Optional[str]
    related_stock_name: Optional[str]
