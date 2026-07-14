import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (4-Line Summary)")

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
        with st.empty():
            for seconds in range(3, 0, -1):
                st.info(f"Analyzing... {seconds}")
                time.sleep(1)
            st.empty()

        with st.spinner('Summarizing...'):
            try:
                # الـ Prompt الجديد هيجبره يكتب 4 سطور بالظبط
                system_prompt = """
                You are a logging assistant. Summarize the chat in EXACTLY 4 lines.
                Use plain, simple English. NO jargon, NO fluff, NO politeness.
                
                Format:
                CST: [Customer issue in simple words]
                Agent: [What I did, short and direct]
                Notes: [Key case details or blockers]
                Status: ended chat since customer not responding
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
                st.text_area("Log:", value=chat_completion.choices[0].message.content, height=200)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
