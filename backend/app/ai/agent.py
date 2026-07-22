from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .tools import *

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

tools = [stock_price, stock_history]

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