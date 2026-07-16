import google.generativeai as genai
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    llm = genai.GenerativeModel(model="gemini-1.5-flash")
else:
    llm = None


def analyze_stock(symbol: str):
    if llm is None:
        return {
            "symbol": symbol,
            "analysis": "GEMINI_API_KEY가 설정되지 않아 기본 응답만 제공합니다.",
        }

    response = llm.generate_content(f"{symbol} 종목에 대한 간단한 분석을 해줘")
    return {"symbol": symbol, "analysis": response.text}


@router.get("/analyze_stock/{symbol}")
def analyze(symbol: str):
    return analyze_stock(symbol)