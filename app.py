import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="스마트 점수판", layout="wide", initial_sidebar_state="collapsed")

# CSS 커스텀 스타일 (디자인 전면 수정)
st.markdown("""
    <style>
    .stApp { background-color: #111; }
    
    /* 타이머 스타일 */
    .timer-display {
        font-size: 100px !important;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        background: #222;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
        border: 2px solid #444;
    }

    /* 공통 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        border: none;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 메인 점수 버튼 (숫자 크게) */
    .red-score button {
        height: 300px !important;
        font-size: 180px !important;
        font-weight: 900 !important;
        background-color: #FF0000 !important;
        border-radius: 20px 20px 0 0 !important;
    }
    
    .blue-score button {
        height: 300px !important;
        font-size: 180px !important;
        font-weight: 900 !important;
        background-color: #0000FF !important;
        border-radius: 20px 20px 0 0 !important;
    }

    /* 취소 버튼 (점수 바로 아래 배정) */
    .undo-btn button {
        height: 60px !important;
        font-size: 20px !important;
        background-color: #333 !important;
        border-radius: 0 0 20px 20px !important;
        margin-top: -2px;
    }

    /* 세트 점수 버튼 */
    .set-btn button {
        height: 100px !important;
        font-size: 50px !important;
        font-weight: bold !important;
        background-color: #444 !important;
        border-radius: 15px !important;
        margin-bottom: 10px;
    }

    /* 중앙 교체 버튼 */
    .swap-btn-container {
        display: flex;
        justify-content: center;
        padding-top: 20px;
    }
    
    /* 입력창 글자 크기 */
    input { 
        font-size: 30px !important; 
        font-weight: bold !important; 
        text-align: center !important; 
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    label { color: #aaa !important; font-size: 18px !important; }
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

# 타이머 로직
if st.session_state.timer_running and st.session_state.timer_seconds > 0:
    time.sleep(1)
    st.session_state.timer_seconds -= 1
    st.rerun()

# --- 타이머 영역 ---
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

mins, secs = divmod(st.session_state.timer_seconds, 60)
st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

# --- 메인 점수판 영역 ---
col1, col2, col3 = st.columns([4, 2, 4])

# A팀 (빨간색)
with col1:
    st.session_state.team_a = st.text_input("TEAM NAME", st.session_state.team_a, key="na")
    st.markdown('<div class="red-score">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_a}", key="ba"):
        st.session_state.score_a += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_a} 점수 취소", key="ua"):
        st.session_state.score_a = max(0, st.session_state.score_a - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 세트 및 교체 (중앙)
with col2:
    st.markdown("<h2 style='text-align: center; color: white; margin-bottom:0;'>SET</h2>", unsafe_allow_html=True)
    st.markdown('<div class="set-btn">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.set_a}", key="sa"):
        st.session_state.set_a += 1
        st.rerun()
    if st.button(f"{st.session_state.set_b}", key="sb"):
        st.session_state.set_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="swap-btn-container">', unsafe_allow_html=True)
    if st.button("🔄 교체", key="sw"):
        st.session_state.team_a, st.session_state.team_b = st.session_state.team_b, st.session_state.team_a
        st.session_state.score_a, st.session_state.score_b = st.session_state.score_b, st.session_state.score_a
        st.session_state.set_a, st.session_state.set_b = st.session_state.set_b, st.session_state.set_a
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# B팀 (파란색)
with col3:
    st.session_state.team_b = st.text_input("TEAM NAME", st.session_state.team_b, key="nb")
    st.markdown('<div class="blue-score">', unsafe_allow_html=True)
    if st.button(f"{st.session_state.score_b}", key="bb"):
        st.session_state.score_b += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
    if st.button(f"↩ {st.session_state.team_b} 점수 취소", key="ub"):
        st.session_state.score_b = max(0, st.session_state.score_b - 1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
