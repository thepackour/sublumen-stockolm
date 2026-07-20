from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from .tools import stock_price

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

tools = [stock_price]

system_prompt = """
너는 주식 투자 도우미이다.

필요한 경우 Tool을 사용하여 답변한다.
모르면 추측하지 말고 Tool을 사용한다.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)
