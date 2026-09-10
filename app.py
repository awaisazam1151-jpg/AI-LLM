import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Universal Study Assistant", page_icon="🧠", layout="centered")

# Access API key securely from Streamlit secrets or environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please configure your GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🧠 Universal AI Study Assistant")
st.write("Ask any topic to receive a detailed, step-by-step explanation from scratch.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter a topic (e.g., 'Calculus', 'Neural Networks')..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Generating explanation..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    "system_instruction": (
                        "You are an expert AI Educator and Mentor. Explain concepts from "
                        "absolute scratch using plain language, structured milestones, and "
                        "relatable real-world analogies. Keep every word purposeful."
                    )
                }
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
