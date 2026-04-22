import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# 2. 스타일 설정 (버튼 색상 및 레이아웃 강제 고정)
st.markdown("""
    <style>
    .stApp { background-color: #111; }
    h2 { color: white !important; text-align: center; margin-bottom: 5px; }
    
    /* 타이머 숫자 스타일 */
    .timer-display {
        font-size: 140px !important;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        background: #222;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        border: 3px solid #444;
        font-family: 'Courier New', monospace;
    }

    /* 팀 점수 버튼 (빨강/파랑) */
    div[data-testid="column"]:nth-of-type(1) button {
        height: 380px !important;
        background-color: #FF0000 !important;
        color: white !important;
        font-size: 220px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
    }
    div[data-testid="column"]:nth-of-type(3) button {
        height: 380px !important;
        background-color: #0000FF !important;
        color: white !important;
        font-size: 220px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
    }

    /* 세트 점수 버튼 */
    div[data-testid="column"]:nth-of-type(2) button {
        height: 100px !important;
        background-color: #333 !important;
        color: white !important;
        font-size: 55px !important;
        font-weight: bold !important;
    }

    /* 상단 설정 라인 버튼 */
    .top-settings button {
        height: 45px !important;
        font-size: 16px !important;
        margin-top: 28px;
    }

    /* 취소 및 교체 버튼 */
    .small-btn-container button {
        height: 60px !important;
        font-size: 20px !important;
        background-color: #444 !important;
        width: 100% !important;
        margin-top: 10px;
    }
    
    /* 입력창 글자 크기 */
    input { font-size: 28px !important; text-align: center !important; }
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

# --- 상단 설정 영역 (한 줄 배치) ---
t_col1, t_col2, t_col3 = st.columns([2, 1, 1])

with t_col1:
    minutes = st.number_input("시간 설정 (분)", min_value=0, value=st.session_state.timer_seconds // 60)
with t_col2:
    st.markdown('<div class="top-settings">', unsafe_allow_html=True)
    if st.button("⚙️ 시간 적용"):
        st.session_state.timer_seconds = minutes * 60
        st.session_state.timer_running = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with t_col3:
    st.markdown('<div class="top-settings">', unsafe_allow_html=True)
    btn_label = "⏸ PAUSE" if st.session_state.timer_running else "▶ START"
    if st.button(btn_label):
        st.session_state.timer_running = not st.session_state.timer_running
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 타이머 숫자판 ---
mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

st.divider()

# --- 메인 점수판 ---
col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    st.session_state.team_a = st.text_input("TEAM A", st.session_state.team_a, key="n_a")
    if st.button(f"{st.session_state.score_a}", key="b_a"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('<div class="small-btn-container">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} 취소", key="u_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h2>SET</h2>", unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="s_a"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="s_b"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('<div class="small-btn-container">', unsafe_allow_html=True)
    if st.button("🔄 교체", key="swap"):
        # 팀명, 점수, 세트 모두 교체
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.session_state.team_b = st.text_input("TEAM B", st.session_state.team_b, key="n_b")
    if st.button(f"{st.session_state.score_b}", key="b_b"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('<div class="small-btn-container">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} 취소", key="u_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
