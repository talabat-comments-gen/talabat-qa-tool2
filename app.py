import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (Strict Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste chat here (No fluff, just data):", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Logging...'):
            try:
                # هذا هو الـ Prompt "الديكتاتوري"
                system_prompt = """
                You are a data logger. Extract facts ONLY.
                STRICTLY FORBIDDEN: Apologies, greetings, polite filler, "I".
                IF NOT STATED IN CHAT, DO NOT WRITE IT.
                
                Format:
                CST: [Problem]
                Agent: [Action 1, Action 2]
                Notes: [Specifics]
                Status: ended chat since customer not responding
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0 # التيمبرتشر 0 بيخليه "ينفذ" الأوامر حرفياً
                )
                
                st.text_area("Final Log (Raw Facts):", value=chat_completion.choices[0].message.content, height=200)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
