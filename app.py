import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# 2. 강력한 스타일 적용 (버튼 색상, 크기, 상단 정렬 강제)
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp { background-color: #111; }
    
    /* [상단 설정바] 숫자입력창과 버튼 높이 통일 및 정렬 */
    div[data-testid="stNumberInput"] {
        height: 60px !important;
    }
    div[data-testid="stNumberInput"] input {
        height: 60px !important;
        font-size: 30px !important;
    }
    
    /* 상단 버튼들 (시간적용, START/PAUSE) 높이 강제 고정 */
    .top-btn-container button {
        height: 60px !important;
        margin-top: 28px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }

    /* 타이머 숫자판 */
    .timer-display {
        font-size: 140px !important;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        background: #222;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        border: 4px solid #444;
        font-family: 'Courier New', monospace;
    }

    /* [중요] 팀별 점수 버튼 색상 및 크기 강제 적용 */
    /* 팀 A (빨강 상자) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        height: 400px !important;
        background-color: #FF0000 !important;
        color: white !important;
        font-size: 250px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 10px #cc0000 !important;
    }

    /* 팀 B (파랑 상자) */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        height: 400px !important;
        background-color: #0000FF !important;
        color: white !important;
        font-size: 250px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 10px #0000cc !important;
    }

    /* 세트 점수 버튼 (중앙) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        height: 130px !important;
        background-color: #444 !important;
        color: white !important;
        font-size: 70px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
    }

    /* 하단 작은 버튼들 (취소, 교체) */
    .lower-btn button {
        height: 60px !important;
        font-size: 22px !important;
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #444 !important;
        margin-top: 10px !important;
    }

    /* 팀 이름 입력창 */
    div[data-testid="stTextInput"] input {
        font-size: 35px !important;
        font-weight: bold !important;
        height: 60px !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 초기화
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a': "A 팀", 'team_b': "B 팀",
        'timer_seconds': 300,
        'timer_running': False
    })

# 4. 타이머 작동 로직
if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

# --- 상단 설정 영역 (한 줄 배치 및 높이 정렬) ---
t_col1, t_col2, t_col3 = st.columns([2, 1, 1])

with t_col1:
    minutes = st.number_input("시간 설정 (분)", min_value=0, value=st.session_state.timer_seconds // 60)
with t_col2:
    st.markdown('<div class="top-btn-container">', unsafe_allow_html=True)
    if st.button("⚙️ 시간 적용"):
        st.session_state.timer_seconds = minutes * 60
        st.session_state.timer_running = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with t_col3:
    st.markdown('<div class="top-btn-container">', unsafe_allow_html=True)
    btn_label = "⏸ PAUSE" if st.session_state.timer_running else "▶ START"
    if st.button(btn_label):
        st.session_state.timer_running = not st.session_state.timer_running
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 타이머 숫자판 ---
mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

st.divider()

# --- 메인 점수판 UI ---
col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    st.session_state.team_a = st.text_input("TEAM NAME", st.session_state.team_a, key="n_a")
    if st.button(f"{st.session_state.score_a}", key="b_a"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('<div class="lower-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} 취소", key="u_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='margin-bottom:0;'>SET</h2>", unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="s_a"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="s_b"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('<div class="lower-btn">', unsafe_allow_html=True)
    if st.button("🔄 교체", key="swap_btn"):
        # 팀명, 점수, 세트 한꺼번에 교체
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.session_state.team_b = st.text_input("TEAM NAME", st.session_state.team_b, key="n_b")
    if st.button(f"{st.session_state.score_b}", key="b_b"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('<div class="lower-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} 취소", key="u_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
