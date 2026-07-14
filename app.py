import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Surgical Engine", layout="centered")
st.title("🚀 Talabat Surgical Extraction (200% Precision)")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=250)

if st.button("Extract Data (Strict & Accurate)"):
    if chat_input:
        with st.spinner('Analyzing chat...'):
            try:
                system_prompt = """
                You are a Literal Translation and Data Extraction Engine.
                
                YOUR MISSION:
                1. Read the provided chat transcript.
                2. Extract ALL unique issues/complaints.
                3. MERGE DUPLICATES: If an issue is mentioned multiple times, list it ONLY ONCE. Each bar MUST be unique.
                4. TRANSLATION: Translate literally from Arabic to English. Do not summarize, do not paraphrase. Maintain the exact meaning.
                5. SYSTEM LIMITATION LOGIC: If the agent cannot act due to system rules or limitations, write EXPLICITLY: 'Action prevented by system limitation'.
                
                FORMAT:
                [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - OUTPUT MUST BE STRICTLY ENGLISH. NO ARABIC CHARACTERS.
                - Order ID: MUST be purely numeric. If the chat mentions a 'Ticket ID', 'Chat ID', or includes letters/dashes/symbols, IGNORE IT and write 'N/A'.
                - Sort by importance.
                - NO intros, NO filler, NO headers. JUST the data lines.
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
