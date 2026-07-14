import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (Simple)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste Chat Transcript Here:", height=400)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Simplifying...'):
            try:
                # ده الـ Prompt الجديد: بسيط، مباشر، بدون أي تأليف
                system_prompt = """
                You are a simple note-taker. 
                Write the log using simple, broken-down English.
                DO NOT add any status codes like 'DELIVERED'.
                DO NOT use formal words like 'escalated'.
                Use this format:
                CST: [Issue in few words] // Agent: [What I did in few words]
                
                Rules:
                1. If I did nothing, write 'NAT'.
                2. No extra explanations. Just the facts.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.code(chat_completion.choices[0].message.content, language=None)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
