from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.container import container
from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=settings.GEMINI_API_KEY
)

stock_tool = container.stock_tool
news_tool = container.news_tool
financial_statement_tool = container.financial_statement_tool
technical_analysis_tool = container.technical_analysis_tool
backtest_tool = container.backtest_tool

tools = (
    stock_tool.get_tools()
    + news_tool.get_tools()
    + financial_statement_tool.get_tools()
    + technical_analysis_tool.get_tools()
    + backtest_tool.get_tools()
)

system_prompt = """
너는 주식 투자 도우미이다.

필요한 경우 Tool을 사용하여 답변한다.
모르면 추측하지 말고 Tool을 사용한다.

기술적 분석 결과는 수익을 보장하는 추천이 아니라 참고자료임을 명확히 설명한다.
백테스트를 미래 성과처럼 표현하지 않는다.

답변은 JSON으로 출력하지 않고 사용자 친화적으로 요약하라.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)
