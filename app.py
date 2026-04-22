import streamlit as st
import time

# 1. 페이지 설정: 다크 모드 및 와이드 레이아웃
st.set_page_config(page_title="초등 체육 스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# 2. 세션 상태 초기화 (데이터 유지)
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a_name': "A 팀", 'team_b_name': "B 팀",
        'timer_seconds': 300,
        'timer_running': False,
        'initial_minutes': 5
    })

# 3. 강력한 CSS 스타일링 (버튼 크기, 색상, 정렬 강제)
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp { background-color: #111111; }
    
    /* 상단 바 높이 정렬 및 입력창 스타일 */
    div[data-testid="stHorizontalBlock"] { align-items: flex-end; }
    
    /* 숫자 입력창 및 버튼 높이 통일 */
    .stNumberInput input { height: 60px !important; font-size: 25px !important; }
    .stButton button { width: 100%; height: 60px; font-weight: bold; font-size: 1.2rem; }

    /* 타이머 숫자판 */
    .timer-container {
        background-color: #222;
        border: 4px solid #444;
        border-radius: 20px;
        text-align: center;
        padding: 10px 0;
        margin: 15px 0;
    }
    .timer-text {
        font-family: 'Courier New', monospace;
        font-size: 180px !important;
        font-weight: 900;
        color: #00FF00; /* 형광 녹색 */
        line-height: 1.2;
    }

    /* 메인 점수판 버튼 스타일 */
    /* 왼쪽 A팀 (빨강) */
    div[data-testid="column"]:nth-of-type(1) .score-btn button {
        height: 450px !important;
        background-color: #FF0000 !important;
        color: white !important;
        font-size: 300px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 10px #880000;
    }
    
    /* 오른쪽 B팀 (파랑) */
    div[data-testid="column"]:nth-of-type(3) .score-btn button {
        height: 450px !important;
        background-color: #0000FF !important;
        color: white !important;
        font-size: 300px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 10px #000088;
    }

    /* 중앙 세트 점수 버튼 */
    .set-btn button {
        height: 120px !important;
        font-size: 60px !important;
        background-color: #333 !important;
        color: white !important;
        margin-bottom: 10px;
    }
    
    /* 팀 이름 입력창 스타일 */
    .team-input input {
        font-size: 40px !important;
        height: 80px !important;
        text-align: center !important;
        font-weight: bold !important;
        background-color: #222 !important;
        color: white !important;
        border: 2px solid #555 !important;
    }

    /* 하단 취소/교체 버튼 */
    .sub-btn button {
        height: 70px !important;
        font-size: 25px !important;
        background-color: #444 !important;
        color: #ddd !important;
    }
    
    /* 텍스트 중앙 정렬 */
    .set-label {
        font-size: 40px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 상단 설정 바
top_col1, top_col2, top_col3, top_col4 = st.columns([2, 1, 1, 1])

with top_col1:
    mins = st.number_input("시간 설정 (분)", min_value=0, max_value=60, value=st.session_state.initial_minutes)
with top_col2:
    if st.button("⚙️ 시간 적용"):
        st.session_state.timer_seconds = mins * 60
        st.session_state.initial_minutes = mins
        st.session_state.timer_running = False
        st.rerun()
with top_col3:
    if st.session_state.timer_running:
        if st.button("⏸ PAUSE"):
            st.session_state.timer_running = False
            st.rerun()
    else:
        if st.button("▶ START"):
            st.session_state.timer_running = True
            st.rerun()
with top_col4:
    if st.button("🔄 초기화"):
        st.session_state.timer_seconds = st.session_state.initial_minutes * 60
        st.session_state.timer_running = False
        st.rerun()

# 5. 타이머 로직 및 표시
if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

m, s = divmod(st.session_state.timer_seconds, 60)
st.markdown(f"""
    <div class="timer-container">
        <div class="timer-text">{m:02d}:{s:02d}</div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 점수판 (3컬럼)
col_a, col_set, col_b = st.columns([4, 2, 4])

# --- 왼쪽 A팀 ---
with col_a:
    st.markdown('<div class="team-input">', unsafe_allow_html=True)
    st.session_state.team_a_name = st.text_input("A팀 이름", st.session_state.team_a_name, key="t_a", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="score-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_a}", key="btn_a"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a_name} 점수 취소", key="undo_a"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 중앙 세트 ---
with col_set:
    st.markdown('<div class="set-label">SET</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="set-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="set_a_btn"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="set_b_btn"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("") # 간격 조절
    st.markdown('<div class="sub-btn">', unsafe_allow_html=True)
    if st.button("🔄 교체"):
        # 데이터 스와프
        st.session_state.team_a_name, st.session_state.team_b_name = st.session_state.team_b_name, st.session_state.team_a_name
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 오른쪽 B팀 ---
with col_b:
    st.markdown('<div class="team-input">', unsafe_allow_html=True)
    st.session_state.team_b_name = st.text_input("B팀 이름", st.session_state.team_b_name, key="t_b", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="score-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_b}", key="btn_b"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b_name} 점수 취소", key="undo_b"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 7. 아이디어 추가: 모든 점수 리셋 (하단 구석)
st.divider()
if st.button("전체 경기 리셋 (점수 및 세트 모두 0으로)"):
    st.session_state.score_a = 0
    st.session_state.score_b = 0
    st.session_state.set_a = 0
    st.session_state.set_b = 0
    st.rerun()
