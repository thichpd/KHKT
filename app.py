import streamlit as st
import google.generativeai as genai

# ================== CẤU HÌNH ==================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

SYSTEM_PROMPT = """
Bạn là 'Thầy giáo ảo Tin Học'.
Nhiệm vụ: hướng dẫn học sinh THPT học Tin học.

Quy tắc:
1. Giải thích tư duy trước khi code.
2. Chỉ ra lỗi nếu code sai.
3. Gợi ý, không cho lời giải ngay.
4. Luôn động viên học sinh.
"""

MODEL_NAME = "gemini-2.5-flash-lite"
MAX_HISTORY = 6

# ================== GIAO DIỆN ==================
st.set_page_config(page_title="Trợ Lý Tin Học THPT")
st.title("🤖 Trợ Lý Học Tập Tin Học")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị lịch sử
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Nhập câu hỏi
user_input = st.chat_input("Em đang gặp khó khăn gì?")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    recent_history = st.session_state.chat_history[-MAX_HISTORY:]

    prompt = SYSTEM_PROMPT + "\n\n"
    for msg in recent_history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    # ===== GỌI GEMINI (CHUẨN) =====
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        reply = f"❌ Lỗi Gemini API: {e}"

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)












