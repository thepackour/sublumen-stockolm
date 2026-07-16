from fastapi import FastAPI

from backend.services.stock_service import router as stock_router

app = FastAPI()

app.include_router(stock_router, prefix="/stocks", tags=["stocks"])