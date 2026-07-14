import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Raw Log", layout="centered")
st.title("🚀 Talabat Raw Log (English Only)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate"):
    if chat_input:
        with st.spinner('Analyzing...'):
            try:
                system_prompt = """
                You are a data extraction engine.
                - Analyze the chat transcript completely.
                - Identify EACH complaint or distinct issue.
                - For EACH issue, output a separate line in this exact format:
                [Issue] // [Details] // [Action] // [Order ID]

                STRICT RULES:
                1. STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS ALLOWED in the result. Translate any Arabic input to English.
                2. [Order ID]: ONLY NUMERIC DIGITS. If it contains letters/dashes/symbols (like Ticket IDs), write 'N/A'.
                3. NO intros, NO titles, NO headers, NO filler. Output ONLY the data lines.
                4. Sort by importance (Most critical issue first).
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # إظهار النتيجة
                st.code(chat_completion.choices[0].message.content, language=None)
                
            except Exception as e:
                st.error(f"Error: {e}")
