from langchain.tools import tool
import FinanceDataReader as fdr
from app.services.stock_service import StockService

stock_service = StockService()


@tool
def stock_price(stock_name: str) -> dict:
    """
    주식 현재가를 조회한다.

    Args:
        stock_name: 종목 이름
    """

    print("stock_price is used.")

    symbol = stock_service.find_symbol(stock_name)

    if symbol is None:
        return {"error": f"No data found for '{stock_name}'"}
    
    result = stock_service.get_stock_price(symbol)

    return result

@tool
def stock_history(
    stock_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    """
    과거 주식 가격을 조회한다.

    Args:
        stock_name: 종목 이름
        start_date: YYYY-MM-DD (optional)
        end_date: YYYY-MM-DD (optional)
    """

    print("stock_history is used.")

    symbol = stock_service.find_symbol(stock_name)
    if symbol is None: return {"error": f"No data found for '{stock_name}'"}
    
    return stock_service.get_stock_history(symbol, start_date, end_date)
