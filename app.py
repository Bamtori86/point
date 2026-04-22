import streamlit as st
import time

# 1. 페이지 설정 (탭에서 보기 좋게 넓은 레이아웃 사용)
st.set_page_config(page_title="교실 점수판", layout="wide", initial_sidebar_state="collapsed")

# 2. 스타일 설정 (버튼 크기 및 가시성 확보)
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 150px;
        font-size: 80px !important;
        font-weight: bold;
    }
    .undo-btn button {
        height: 50px !important;
        font-size: 18px !important;
        background-color: #f0f2f6;
    }
    .timer-text {
        font-size: 100px !important;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 초기화 (점수 및 팀명 데이터 유지)
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a': "A 팀", 'team_b': "B 팀",
        'timer_running': False
    })

# --- 주요 기능 함수 ---
def change_court():
    st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
    st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
    st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a

# --- 화면 구성 ---
st.title("⏱️ 스마트 교실 점수판")

# 설명서 (도움말)
with st.expander("📖 사용 설명서 (터치해서 열기)"):
    st.info("""
    - **점수 올리기:** 큰 숫자 버튼을 터치하세요.
    - **점수 취소:** 숫자 아래 '점수 취소' 버튼을 누르세요.
    - **코트 체인지:** 중앙의 화살표 버튼을 누르면 팀 정보가 서로 바뀝니다.
    - **타이머:** 분을 설정하고 '시작/정지'를 누르세요.
    """)

# [상단] 타이머 섹션
col_t1, col_t2 = st.columns([1, 1])
with col_t1:
    set_min = st.number_input("시간 설정 (분)", min_value=0, value=5)
with col_t2:
    st.write("## ") # 간격 조절
    if st.button("⏯️ 시작 / 일시정지"):
        st.session_state.timer_running = not st.session_state.timer_running

st.divider()

# [중앙] 메인 스코어보드
col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    st.session_state.team_a = st.text_input("팀 1", st.session_state.team_a)
    if st.button(f"{st.session_state.score_a}", key="score_a_btn"):
        st.session_state.score_a += 1
        st.rerun()
    if st.button(f"↩ {st.session_state.team_a} 점수 취소", key="undo_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()

with col2:
    st.write("### 세트")
    st.write(f"## {st.session_state.set_a} : {st.session_state.set_b}")
    if st.button("🔄"):
        change_court()
        st.rerun()

with col3:
    st.session_state.team_b = st.text_input("팀 2", st.session_state.team_b)
    if st.button(f"{st.session_state.score_b}", key="score_b_btn"):
        st.session_state.score_b += 1
        st.rerun()
    if st.button(f"↩ {st.session_state.team_b} 점수 취소", key="undo_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
