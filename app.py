import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Log", layout="centered")
st.title("🚀 Talabat Log Engine")

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
        with st.spinner('Summarizing...'):
            try:
                # الـ Prompt الجديد صارم جداً
                system_prompt = """
                You are a Talabat agent writing a simple log.
                Format: 
                CST: [The issue] // Agent: [I + actions, separated by commas] // Status: [Final state]

                Rules:
                1. Use very simple English.
                2. NO status codes (e.g., NO 'DELIVERED', NO 'R-OD').
                3. If customer stops responding, write: 'ended chat since customer not responding'.
                4. Do not be polite or professional, be direct and fast.
                5. Use 'I' for agent actions.
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
