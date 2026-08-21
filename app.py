import streamlit as st
from google import genai

st.set_page_config(page_title="Trợ Lý Gemini", page_icon="🤖", layout="wide")
st.title("🤖 Trợ Lý AI")

# Menu bên trái
with st.sidebar:
    st.header("Cài đặt")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    
    # Cho phép chọn model trực tiếp
    model_name = st.selectbox(
        "Chọn Model AI:",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
    )
    
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại tin nhắn cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý khi gửi tin nhắn
if prompt := st.chat_input("Nhập câu hỏi, kịch bản..."):
    if not api_key:
        st.warning("Vui lòng nhập API Key ở menu bên trái để bắt đầu.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            reply = response.text

            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Lỗi: {e}")
