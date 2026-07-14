import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat Raw Log", layout="centered")
st.title("🚀 Talabat Raw Log (Mirror Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# الشات بار زي ما طلبت
chat_input = st.text_area("Paste chat here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        # العد التنازلي
        with st.empty():
            for seconds in range(3, 0, -1):
                st.info(f"Analyzing... {seconds}")
                time.sleep(1)
            st.empty()

        with st.spinner('Extracting...'):
            try:
                # الـ Prompt ده "حرفي" جداً وممنوع فيه التجويد
                system_prompt = """
                You are a literal logging machine. 
                1. Read the chat and list EXACT events as they happened.
                2. Do NOT paraphrase, do NOT summarize, and do NOT use professional jargon.
                3. If the agent did not say a specific thing, DO NOT write it.
                4. Agent Actions: List what actually happened (e.g., 'asked for photo', 'checked order').
                5. Format strictly:
                CST: [User issue keywords] // Agent: [Actual actions] // Status: [Outcome]
                6. If the chat ended because of no response: 'ended chat since customer not responding'.
                7. English only. No politeness. No 'I'.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # الكومنت بار أطول
                st.text_area("Log:", value=chat_completion.choices[0].message.content, height=250)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
