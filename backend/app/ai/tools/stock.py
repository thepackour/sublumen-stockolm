from langchain.tools import tool

@tool
def stock_price(symbol: str) -> str:
    """주식 현재가를 조회한다."""

    dummy = {
        "005930": "삼성전자 현재가는 75,200원입니다.",
        "AAPL": "애플 현재가는 210달러입니다."
    }

    return dummy.get(symbol, "해당 종목을 찾을 수 없습니다.")