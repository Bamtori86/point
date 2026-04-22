import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# CSS 스타일: 버튼 디자인과 타이머를 전면 수정
st.markdown("""
    <style>
    .stApp { background-color: #111; }
    
    /* 타이머 스타일: 시계 이미지 느낌 */
    .timer-display {
        font-size: 140px !important;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        background: #222;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 4px solid #444;
        font-family: 'monospace';
    }

    /* 메인 점수 상자 스타일 (빨강/파랑 강제 적용) */
    div.stButton > button {
        width: 100% !important;
        border: none !important;
        color: white !important;
        font-weight: 900 !important;
    }

    /* 팀 A 빨간 버튼 */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        height: 350px !important;
        font-size: 200px !important;
        background-color: #FF0000 !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.4);
    }
    
    /* 팀 B 파란 버튼 */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        height: 350px !important;
        font-size: 200px !important;
        background-color: #0000FF !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 255, 0.4);
    }

    /* 세트 점수 버튼 (중앙) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        height: 120px !important;
        font-size: 60px !important;
        background-color: #333 !important;
        margin-bottom: 10px;
    }

    /* 취소 및 교체 버튼 스타일 */
    .small-btn div.stButton > button {
        height: 60px !important;
        font-size: 20px !important;
        background-color: #222 !important;
        border: 1px solid #444 !important;
        margin-top: 10px;
    }

    /* 입력창 디자인 */
    input { 
        font-size: 28px !important; 
        text-align: center !important; 
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'score_a' not in st.session_state:
    st.session_state.update({
        'score_a': 0, 'score_b': 0,
        'set_a': 0, 'set_b': 0,
        'team_a': "A 팀", 'team_b': "B 팀",
        'timer_seconds': 300,
        'timer_running': False
    })

# --- 타이머 및 설정 영역 ---
col_t1, col_t2 = st.columns([1, 1])
with col_t1:
    minutes = st.number_input("시간 설정 (분)", min_value=0, value=st.session_state.timer_seconds // 60)
    if st.button("⚙️ 시간 적용"):
        st.session_state.timer_seconds = minutes * 60
        st.session_state.timer_running = False
        st.rerun()

with col_t2:
    st.write("## ")
    if st.button("▶ START / ⏸ PAUSE"):
        st.session_state.timer_running = not st.session_state.timer_running
        st.rerun()

# 실시간 시계 표시 및 작동 로직
mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

# --- 메인 점수판 (3컬럼 레이아웃) ---
col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    st.session_state.team_a = st.text_input("TEAM NAME", st.session_state.team_a, key="na")
    if st.button(f"{st.session_state.score_a}", key="ba"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} 취소", key="ua"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='text-align: center; color: white;'>SET</h2>", unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="sa"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="sb"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button("🔄 교체", key="sw"):
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.session_state.team_b = st.text_input("TEAM NAME", st.session_state.team_b, key="nb")
    if st.button(f"{st.session_state.score_b}", key="bb"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} 취소", key="ub"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
