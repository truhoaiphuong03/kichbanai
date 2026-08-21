import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Trợ Lý AI", page_icon="🤖", layout="wide")
st.title("🤖 Trợ Lý Gemini Riêng")

# Menu bên trái
with st.sidebar:
    st.header("Cài đặt")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý tin nhắn
if prompt := st.chat_input("Nhập yêu cầu, kịch bản, câu hỏi..."):
    if not api_key:
        st.warning("Vui lòng nhập API Key ở menu bên trái để bắt đầu.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            genai.configure(api_key=api_key)
            
            # Tự động lấy danh sách model hỗ trợ tạo nội dung trong tài khoản
            available_models = [
                m.name for m in genai.list_models() 
                if "generateContent" in m.supported_generation_methods
            ]
            
            # Ưu tiên chọn model flash hoặc lấy model đầu tiên khả dụng
            chosen_model = next((m for m in available_models if "flash" in m), available_models[0])
            
            model = genai.GenerativeModel(chosen_model)
            response = model.generate_content(prompt)
            reply = response.text

            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Lỗi: {e}")
