import os
from datetime import datetime

import requests
import streamlit as st

st.set_page_config(page_title="Stock-olm", page_icon="📈", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@st.cache_data(show_spinner=False)
def fetch_json(path: str):
    try:
        response = requests.get(f"{BACKEND_URL}{path}", timeout=8)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def post_json(path: str, payload: dict):
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=8)
        print(response.status_code) ################################
        print(response.text)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def post_chat_message(question: str):
    return post_json("/api/v1/chat", {"question": question})


st.title("Stock-olm")
st.caption("주식 초보의 든든한 도우미, Stock-olm")
st.markdown(
    "주식 시장에 첫발을 내딛는 사람들에게, 데이터·뉴스·시뮬레이션을 한 화면에서 살펴볼 수 있는 경험을 제공합니다."
)

with st.sidebar:
    st.header("서비스 탐색")
    st.selectbox("시장 유형", ["국내주식", "해외주식", "ETF", "환율"], key="market")
    symbol = st.text_input("종목 코드", value="005930", max_chars=10)
    if st.button("분석 요청", use_container_width=True):
        st.session_state["symbol"] = symbol.upper()

    st.markdown("---")
    st.subheader("우선순위 1 기능")
    st.write("• 종목 검색")
    st.write("• 환율 조회")
    st.write("• 재무제표 조회")
    st.write("• 뉴스 조회")
    st.write("• 분석 요청/조회")
    st.write("• 백테스트 실행/조회")

selected_symbol = st.session_state.get("symbol", symbol.upper())
stock_data = fetch_json(f"/api/v1/stocks/{selected_symbol}")
financials = fetch_json(f"/api/v1/stocks/{selected_symbol}")
exchange_rates = fetch_json("/api/v1/exchange-rates")
news = fetch_json("/api/v1/news")
analysis_result = post_json("/api/v1/analysis", {"symbol": selected_symbol, "analysis_type": "summary"})
backtest_result = post_json("/api/v1/backtests", {"symbol": selected_symbol, "strategy": "buy_and_hold", "initial_capital": 1000000})

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("현재 종목", stock_data.get("symbol", selected_symbol))
with col2:
    st.metric("환율 정보", str(exchange_rates.get("items", [{}])[0].get("pair", "-")))
with col3:
    st.metric("백테스트 수익률", f"{backtest_result.get('returnRate', 0)}%")

st.markdown("---")

st.subheader("오늘의 투자 여정")
main_tab, roadmap_tab, portfolio_tab, chat_tab = st.tabs(["핵심 데이터", "기능 로드맵", "포트폴리오 시나리오", "AI 챗봇 테스트"])

with main_tab:
    st.info(f"현재 조회 중인 종목: {selected_symbol}")

    st.subheader("종목 정보")
    if "error" in stock_data:
        st.warning("백엔드 연결을 확인해 주세요.")
    else:
        st.write(stock_data)

    st.subheader("재무제표")
    st.write(financials)

    st.subheader("환율")
    st.write(exchange_rates)

    st.subheader("뉴스")
    for item in news.get("items", []):
        with st.expander(item.get("title", "뉴스")):
            st.write(item.get("summary", ""))
            st.caption(f"출처: {item.get('source', 'unknown')}")

    st.subheader("분석 결과")
    st.write(analysis_result)

    st.subheader("백테스트 결과")
    st.write(backtest_result)

with roadmap_tab:
    st.markdown("### 1단계 (MVP)")
    st.write("- 종목 검색/상세 조회")
    st.write("- 환율, 재무제표, 뉴스 조회")
    st.write("- 분석 요청/백테스트 실행")

    st.markdown("### 2단계")
    st.write("- 전략 비교")
    st.write("- 포트폴리오 구성")
    st.write("- 리서치 및 실시간 데이터")

with portfolio_tab:
    st.write("포트폴리오 구성, 리스크 관리, 시뮬레이션 결과는 이 영역에서 확장됩니다.")
    st.progress(40)
    st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with chat_tab:
    st.subheader("AI 챗봇 테스트")
    st.write("백엔드의 /api/v1/chat 엔드포인트로 질문을 보내고 응답을 확인합니다.")

    chat_question = st.text_area(
        "질문을 입력하세요",
        placeholder="예: 삼성전자 종목에 대해 간단히 분석해줘",
        height=120,
    )

    if st.button("질문 보내기", use_container_width=True):
        if not chat_question.strip():
            st.warning("질문을 입력해 주세요.")
        else:
            with st.spinner("응답을 기다리는 중입니다..."):
                chat_result = post_chat_message(chat_question.strip())

            if "error" in chat_result:
                st.error(f"요청 실패: {chat_result['error']}")
            else:
                st.success("응답을 받았습니다.")
                st.markdown("### 답변")
                st.write(chat_result.get("answer", "응답이 없습니다."))
