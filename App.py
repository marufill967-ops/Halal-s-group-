import streamlit as st
import requests

MODEL = "gemini-3.6-flash"

st.set_page_config(page_title="Amar Bot")
st.title("🤖 Amar Bot")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = ""

if not API_KEY:
    API_KEY = st.sidebar.text_input("Gemini API Key", type="password").strip()

if not API_KEY:
    st.sidebar.text_input("Gemini API Key")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def ask_gemini(history):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    contents = [
        {
            "role": "user" if m["role"] == "user" else "model",
            "parts": [{"text": m["content"]}],
        }
        for m in history
    ]
    try:
        res = requests.post(
            url,
            headers={"x-goog-api-key": API_KEY},
            json={"contents": contents},
            timeout=60,
        )
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection somossa: {e}"

    try:
        j = res.json()
    except ValueError:
        return f"⚠️ Bujhte pari emon uttor ashe nai (status {res.status_code})"

    if res.status_code != 200:
        msg = j.get("error", {}).get("message", str(j))
        return f"⚠️ Google error ({res.status_code}): {msg}"

    try:
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return f"⚠️ Bot kono uttor dey nai. Details: {j}"


if prompt := st.chat_input("Kisu jigges koro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Bhabchi..."):
            reply = ask_gemini(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
