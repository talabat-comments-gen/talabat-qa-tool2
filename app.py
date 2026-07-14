import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat 200% Precision Engine", layout="centered")
st.title("🚀 Talabat 200% Precision Engine")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=250)

if st.button("Extract (200% Accuracy)"):
    if chat_input:
        with st.spinner('Translating & Analyzing...'):
            try:
                system_prompt = """
                You are a Literal Translation and Data Extraction Engine.
                
                YOUR MISSION:
                1. Read the provided chat transcript.
                2. Extract all distinct issues/complaints.
                3. STRICT REQUIREMENT: Identify duplicate issues and merge them. NO DUPLICATE BARS. Each bar must represent a unique, non-repetitive point.
                4. Translation: Translate EVERYTHING from Arabic to English LITERALLY. Use the exact equivalent word. Do not summarize, do not interpret. Keep the original vocabulary tone.
                5. Output format: [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS IN OUTPUT.
                - Order ID: MUST be purely numeric (digits only). If the chat mentions a 'Ticket ID' or includes letters/dashes/symbols, IGNORE IT and write 'N/A'.
                - Sort by importance.
                - NO intros, NO filler, NO headers, NO explanations.
                - Each unique issue MUST be on a separate line.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # إظهار النتائج
                raw_output = chat_completion.choices[0].message.content
                lines = [line.strip() for line in raw_output.split('\n') if line.strip()]
                
                # عرض كل بار منفصل ومعاه زرار الـ Copy تلقائياً
                for line in lines:
                    st.code(line, language=None)
                
            except Exception as e:
                st.error(f"Error: {e}")
