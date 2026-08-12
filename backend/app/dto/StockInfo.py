from pydantic.dataclasses import dataclass


@dataclass
class StockInfo:
    symbol: str
    name: str
    market: str
    sector: str | None
    industry: str | None
