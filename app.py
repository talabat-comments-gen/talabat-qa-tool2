import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Multi-Point Logger", layout="centered")
st.title("🚀 Talabat Multi-Point Logger")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Analyzing all points...'):
            try:
                system_prompt = """
                You are a data extraction engine.
                - Analyze the chat transcript completely.
                - Identify ALL distinct issues, complaints, or comments.
                - Sort them by priority/importance (Most critical issue first).
                - For EACH issue, output a separate line in this format:
                [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                1. STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS ALLOWED.
                2. [Order ID]: ONLY NUMERIC DIGITS. If it contains letters/dashes/symbols (like Ticket IDs), write N/A.
                3. [Details]: English summary + short quote from the chat (translated to English).
                4. [Action]: Summary of agent's action in English.
                5. NO headers, NO greetings, NO filler, NO 'Denied' labels. JUST the data lines.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.text_area("Data Lines:", value=chat_completion.choices[0].message.content, height=150)
                
            except Exception as e:
                st.error(f"Error: {e}")
