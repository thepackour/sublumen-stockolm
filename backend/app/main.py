from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.container import container

from app.api.v1.stock import router as stock_router
from app.api.v1.news import router as news_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.backtest import router as backtest_router
from app.api.v1.chat import router as chat_router
from app.core.database import engine
from app.schedulers.news_collect_scheduler import start_scheduler, shutdown_scheduler, register_jobs

from app.core.handlers import register_exception_handlers
from app.schemas import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    container.initialize()

    register_jobs()
    start_scheduler()
    register_exception_handlers()
    try:
        yield
    finally:
        container.shutdown()
        shutdown_scheduler()

app = FastAPI(title="Sublumen Stockolm API", lifespan=lifespan)

register_exception_handlers(app)

app.include_router(stock_router)
app.include_router(news_router)
app.include_router(analysis_router)
app.include_router(backtest_router)
app.include_router(chat_router)