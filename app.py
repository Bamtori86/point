import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="프리미엄 스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS 스타일 적용 (색상, 정렬, 크기 최적화)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp { background-color: #0E1117; }
    
    /* 상단 컨트롤바 정렬 */
    .top-bar {
        display: flex;
        align-items: flex-end;
        gap: 10px;
    }

    /* 타이머 디스플레이 */
    .timer-display {
        font-size: 120px !important;
        font-weight: 900;
        text-align: center;
        color: #00FF00; /* 네온 그린 */
        background: #1E1E1E;
        border-radius: 20px;
        padding: 10px;
        margin: 20px 0;
        border: 5px solid #333;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    }

    /* 모든 버튼 기본 설정 */
    .stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        transition: all 0.2s;
    }

    /* 팀 A 점수 버튼 (빨강) */
    div[data-testid="column"]:nth-of-type(1) .score-btn button {
        height: 350px !important;
        background-color: #D32F2F !important; /* 강렬한 레드 */
        color: white !important;
        font-size: 200px !important;
        border: none !important;
    }

    /* 팀 B 점수 버튼 (파랑) */
    div[data-testid="column"]:nth-of-type(3) .score-btn button {
        height: 350px !important;
        background-color: #1976D2 !important; /* 강렬한 블루 */
        color: white !important;
        font-size: 200px !important;
        border: none !important;
    }

    /* 중앙 세트 영역 */
    .set-container {
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    
    .set-label {
        font-size: 40px !important;
        font-weight: 900 !important;
        color: white;
        margin-bottom: 10px;
    }

    /* 세트 점수 버튼 */
    .set-btn-a button {
        background-color: #D32F2F !important;
        font-size: 50px !important;
        height: 100px !important;
        margin-bottom: 5px !important;
    }
    .set-btn-b button {
        background-color: #1976D2 !important;
        font-size: 50px !important;
        height: 100px !important;
    }

    /* 하단 보조 버튼 (취소, 교체) */
    .aux-btn button {
        height: 60px !important;
        font-size: 20px !important;
        background-color: #333 !important;
        color: #BBB !important;
        margin-top: 10px !important;
    }

    /* 팀 이름 입력창 스타일링 */
    div[data-testid="stTextInput"] input {
        font-size: 30px !important;
        height: 70px !important;
        text-align: center !important;
        background-color: #262730 !important;
        color: white !important;
        border: 2px solid #444 !important;
    }
    
    /* 숫자 입력창 높이 조절 */
    div[data-testid="stNumberInput"] { margin-bottom: 0px !important; }
    
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 초기화
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a': "TEAM A", 'team_b': "TEAM B",
        'timer_seconds': 300,
        'initial_seconds': 300,
        'timer_running': False
    })

# 4. 타이머 작동 로직
if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

# --- 상단 설정 영역 (정렬 최적화) ---
t_col1, t_col2, t_col3, t_col4 = st.columns([2, 1, 1, 1])

with t_col1:
    new_mins = st.number_input("분 설정", min_value=0, value=st.session_state.initial_seconds // 60)
with t_col2:
    st.write(" ") # 수직 정렬용 여백
    if st.button("⚙️ 시간 적용"):
        st.session_state.timer_seconds = new_mins * 60
        st.session_state.initial_seconds = new_mins * 60
        st.session_state.timer_running = False
        st.rerun()
with t_col3:
    st.write(" ")
    btn_label = "⏸ PAUSE" if st.session_state.timer_running else "▶ START"
    if st.button(btn_label):
        st.session_state.timer_running = not st.session_state.timer_running
        st.rerun()
with t_col4:
    st.write(" ")
    if st.button("⏹ STOP/RESET"):
        st.session_state.timer_seconds = st.session_state.initial_seconds
        st.session_state.timer_running = False
        st.rerun()

# --- 타이머 숫자판 ---
mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

# --- 메인 점수판 UI ---
col_left, col_mid, col_right = st.columns([4, 2, 4])

# 왼쪽 팀 (A)
with col_left:
    st.session_state.team_a = st.text_input("TEAM A NAME", st.session_state.team_a, key="in_a", label_visibility="collapsed")
    st.markdown('<div class="score-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_a}", key="btn_score_a"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="aux-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} -1", key="undo_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 중앙 (세트 및 교체)
with col_mid:
    st.markdown('<div class="set-container">', unsafe_allow_html=True)
    st.markdown('<div class="set-label">SET</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="set-btn-a">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="btn_set_a"):
        st.session_state.set_a += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="set-btn-b">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_b}", key="btn_set_b"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="aux-btn">', unsafe_allow_html=True)
    if st.button("🔄 SWAP", key="swap_btn"):
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 오른쪽 팀 (B)
with col_right:
    st.session_state.team_b = st.text_input("TEAM B NAME", st.session_state.team_b, key="in_b", label_visibility="collapsed")
    st.markdown('<div class="score-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_b}", key="btn_score_b"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="aux-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} -1", key="undo_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
