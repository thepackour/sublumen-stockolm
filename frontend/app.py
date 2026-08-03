print("========== APP START ==========")

import os

import requests
import streamlit as st

st.set_page_config(page_title="Stock-olm", page_icon="📈", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@st.cache_data(show_spinner=False)
def fetch_json(path: str, params: dict):
    try:
        print("GET 요청 날림!!!!!!!!!!!")
        response = requests.get(
            f"{BACKEND_URL}{path}",
            params=params,
            timeout=8)
        print(response.url)
        print(response.status_code)
        print(response.text)
        print("raise_for_status() 실행 전!!!!!!!!!!!")
        response.raise_for_status()
        print("raise_for_status() 실행 후!!!!!!!!!!!")
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def post_json(path: str, payload: dict):
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def post_chat_message(question: str):
    return post_json("/api/v1/chat", {"question": question})

def get_news(query, page, size=10):
    print("get_news() 실행됨!!!!!!!!!!!!!")
    return fetch_json("/api/v1/news", {"query": query, "page": int(page), "size": int(size)})


st.title("Stock-olm")
st.markdown(
    "주식 초보의 든든한 도우미, Stock-olm"
)

with st.sidebar:
    st.header("서비스")
    st.selectbox("목록", ["종목", "포트폴리오", "백테스트"], key="service")

st.markdown("---")

st.subheader("오늘의 투자 여정")
roadmap_tab, search_tab, chat_tab = st.tabs(["기능 로드맵", "검색", "AI 챗봇 테스트"])

with roadmap_tab:
    st.markdown("### 1단계 (MVP)")
    st.write("- 종목 검색/상세 조회")
    st.write("- 환율, 재무제표, 뉴스 조회")
    st.write("- 분석 요청/백테스트 실행")

    st.markdown("### 2단계")
    st.write("- 전략 비교")
    st.write("- 포트폴리오 구성")
    st.write("- 리서치 및 실시간 데이터")

with search_tab:
    st.subheader("검색")
    st.write("주가, 뉴스, 레포트 등등을 검색합니다.")

    st.markdown("### 키워드로 뉴스 검색")
    st.write("GET /api/v1/news")

    with st.container():
        query = st.text_input(
            label="예: 검색어를 입력하세요",
            placeholder="삼성전자",
        )
        page = int(st.number_input(
            label="page",
            placeholder="예: 1",
            width=50,
        ))
        size = int(st.number_input(
            label="size",
            placeholder="예: 10",
            width=50
        ))

    if st.button("실행"):
        print("버튼 눌림!!!!!!!!!!!!!!")
        if not query.strip():
            st.warning("검색어를 입력해 주세요.")
        else:
            print("검색어 있음!!!!!!!!!!!!!!")
            with st.spinner("응답을 기다리는 중입니다..."):
                result = get_news(query.strip(), page, size)
                print("result.values: ", result.values())
            if "error" in result:
                st.error(f"요청 실패: {result['error']}")
            elif int(result["status"]) >= 400:
                st.error(f"요청 실패: {result['message']}")
            else:
                st.success("응답을 받았습니다.")
                st.markdown("### 응답")
                data = result["data"]
                st.write("데이터 수:", data["count"])
                for i in data["items"]:
                    for stock in result:
                        st.write(result.get("data", "응답이 없습니다."))



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
