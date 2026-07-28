from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.clients.fdr_client import StockSymbolService
from app.core.database import SessionLocal
from app.services.stock_service import StockService
from app.repositories.postgres_stock_repository import StockRepository
from app.ai.tools.stock_tools import StockTool


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

stock_repository = StockRepository(SessionLocal)
stock_symbol_service = StockSymbolService()
stock_symbol_service.initialize()
stock_service = StockService(stock_repository, stock_symbol_service)

stock_tool = StockTool(stock_service, stock_symbol_service)

tools = [
    stock_tool.stock_price,
    stock_tool.stock_history
]

system_prompt = """
너는 주식 투자 도우미이다.

필요한 경우 Tool을 사용하여 답변한다.
모르면 추측하지 말고 Tool을 사용한다.

답변은 JSON으로 출력하지 않고 사용자 친화적으로 요약하라.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)