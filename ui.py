import streamlit as st
import requests

st.title("🤖 AI Support Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # بنكلم الـ FastAPI اللي شغال في الـ Terminal التاني
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt})
        if response.status_code == 200:
            res_data = response.json()["data"]
            reply = f"**Issue:** {res_data['issue_type']}\n\n{res_data['suggested_reply']}"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})