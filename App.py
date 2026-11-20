import streamlit as st
import requests

st.set_page_config(page_title="Amar Bot")
st.title("🤖 Amar Bot")

# API Key - Secrets theke nibe
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = st.sidebar.text_input("Gemini API Key dao", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Kisu jigges koro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, json=data, timeout=30)
        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
