from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')

class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    count: int
    page: int
    size: int
    total_count: int