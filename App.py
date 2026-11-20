import streamlit as st
import requests

st.set_page_config(page_title="Amar Bot")
st.title("🤖 Amar Bot")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.success("Key paisi ✅")
except:
    API_KEY = ""
    st.error("Secrets e Key pai nai ❌")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Kisu jigges koro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    res = requests.post(url, json=data, timeout=30)
    j = res.json()
    
    if "candidates" in j:
        reply = j["candidates"][0]["content"]["parts"][0]["text"]
    else:
        reply = f"Google bollo: {j}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
