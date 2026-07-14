import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Data Logger", layout="centered")
st.title("🚀 Talabat Data Logger (Schema Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste chat here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Parsing data...'):
            try:
                # الـ Prompt الجديد مجبر على اتباع الـ Schema بتاعك حرفياً
                system_prompt = """
                You are a data extraction engine. Output ONLY the data in this exact schema. 
                DO NOT write conversational sentences, apologies, or intros.
                
                Format:
                [CST Request] // [Issue Type] // [Details] // [Action/Result] // [System Error Info] // [CST Info]
                
                Rules:
                1. If any field is missing from the chat, write 'N/A'.
                2. If there is a JSON error from the system, copy it exactly as is.
                3. Do NOT add any extra text outside of the schema.
                4. Be concise and technical.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.text_area("Result:", value=chat_completion.choices[0].message.content, height=150)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
