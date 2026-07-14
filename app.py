import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat 200% Precision", layout="centered")
st.title("🚀 Talabat Extraction (Precision 200%)")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here (Arabic/English):", height=250)

if st.button("Extract Data (Literal & Accurate)"):
    if chat_input:
        with st.spinner('Translating & Extracting...'):
            try:
                # الـ Prompt الجديد بتركيز على الترجمة الحرفية والصرامة
                system_prompt = """
                You are a Literal Translation and Data Extraction Engine. 
                
                YOUR MISSION:
                1. Read the provided chat transcript.
                2. Extract all distinct issues/complaints.
                3. Translate EVERYTHING from Arabic to English LITERALLY. Do not summarize. Do not change tone. Maintain the exact meaning of every word.
                4. Output format: [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS IN OUTPUT.
                - Order ID: MUST be purely numeric (digits only). If the chat mentions a 'Ticket ID' or includes letters/dashes/symbols, IGNORE IT and write 'N/A'.
                - Sort by importance.
                - NO intros, NO filler, NO headers, NO explanations.
                - Each issue MUST be on a separate line.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                raw_output = chat_completion.choices[0].message.content
                lines = [line.strip() for line in raw_output.split('\n') if line.strip()]
                
                # عرض النتائج في بارات مع زر الـ Copy
                for line in lines:
                    st.code(line, language=None)
                
            except Exception as e:
                st.error(f"Error: {e}")
