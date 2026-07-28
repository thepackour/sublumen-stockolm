from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.stock import router as stock_router
from app.api.v1.news import router as news_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.backtest import router as backtest_router
from app.api.v1.chat import router as chat_router

from app.core.handlers import register_exception_handlers
from app.clients.fdr_client import StockSymbolService

stock_symbol_service = StockSymbolService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    stock_symbol_service.initialize()
    yield

app = FastAPI(title="Sublumen Stockolm API", lifespan=lifespan)

register_exception_handlers(app)

app.include_router(stock_router)
app.include_router(news_router)
app.include_router(analysis_router)
app.include_router(backtest_router)
app.include_router(chat_router)