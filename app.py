import streamlit as st
import time

# 페이지 설정 (전체 화면 사용)
st.set_page_config(page_title="스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# CSS 커스텀 스타일 (모바일/태블릿 최적화)
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp { background-color: #111; }
    
    /* 타이머 숫자 스타일 */
    .timer-display {
        font-size: 120px !important;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        background: #333;
        border-radius: 20px;
        margin: 10px 0;
        padding: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 점수 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        border: none;
        color: white !important;
    }
    
    /* 빨간색 팀 버튼 (A팀) */
    .red-btn button {
        height: 250px !important;
        font-size: 150px !important;
        background-color: #FF4B4B !important;
    }
    
    /* 파란색 팀 버튼 (B팀) */
    .blue-btn button {
        height: 250px !important;
        font-size: 150px !important;
        background-color: #1E88E5 !important;
    }
    
    /* 세트 점수 버튼 */
    .set-btn button {
        height: 80px !important;
        font-size: 40px !important;
        background-color: #444 !important;
    }
    
    /* 점수 취소 버튼 (가로로 길고 세로로 얇게) */
    .undo-btn button {
        height: 50px !important;
        font-size: 20px !important;
        background-color: #555 !important;
        margin-top: 5px;
    }
    
    /* 텍스트 입력창 흰색으로 */
    input { font-size: 25px !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a': "A 팀", 'team_b': "B 팀",
        'timer_seconds': 300,
        'timer_running': False,
        'last_tick': time.time()
    })

# 타이머 로직
if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

# 상단: 타이머 컨트롤
col_t1, col_t2 = st.columns([1, 1])
with col_t1:
    minutes = st.number_input("분 설정", min_value=0, value=st.session_state.timer_seconds // 60)
    if st.button("⏱ 시간 세팅"):
        st.session_state.timer_seconds = minutes * 60
        st.session_state.timer_running = False
        st.rerun()

with col_t2:
    st.write("## ")
    if st.button("▶ 시작 / ⏸ 일시정지"):
        st.session_state.timer_running = not st.session_state.timer_running
        st.rerun()

# 실시간 시계 이미지 느낌의 숫자 표시
mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

st.divider()

# 메인 점수판 레이아웃
col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    st.session_state.team_a = st.text_input("TEAM A", st.session_state.team_a, key="name_a")
    st.markdown('<div class="red-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_a}", key="btn_a"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} 취소", key="u_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='text-align: center; color: white;'>SET</h3>", unsafe_allow_html=True)
    st.markdown('<div class="set-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="s_a"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="s_b"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 교체", key="swap"):
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()

with col3:
    st.session_state.team_b = st.text_input("TEAM B", st.session_state.team_b, key="name_b")
    st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_b}", key="btn_b"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} 취소", key="u_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
