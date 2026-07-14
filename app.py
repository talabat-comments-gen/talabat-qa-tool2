import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Surgical Engine v2", layout="centered")
st.title("🚀 Talabat Surgical Extraction (v2)")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=250)

if st.button("Extract Data (Detailed & Unique)"):
    if chat_input:
        with st.spinner('Analyzing nuances...'):
            try:
                system_prompt = """
                You are a Surgical Data Extraction Engine.
                
                YOUR MISSION:
                1. Read the provided chat transcript.
                2. Deconstruct the conversation into 4 distinct, detailed, and unique data points (nuances):
                   - Point 1: The core issue/fact (The "What").
                   - Point 2: The customer's emotional response or specific feedback (The "How").
                   - Point 3: The agent's specific technical response or limitation (The "Why").
                   - Point 4: The outcome or next step (The "Result").
                3. STRICT REQUIREMENT: Ensure each of the 4 points is unique and uses different phrasing. Do not repeat.
                4. TRANSLATION: Literal English translation only. Do not summarize, maintain the exact tone.
                5. SYSTEM LOGIC: If the agent is restricted by the system, ALWAYS use the phrase: 'no action taken'.
                
                FORMAT:
                [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS.
                - Order ID: MUST be purely numeric. If the chat mentions a 'Ticket ID' or includes letters/dashes, IGNORE IT and write 'N/A'.
                - Sort by importance (Most critical first).
                - NO intros, NO filler, NO headers. JUST the 4 distinct data lines.
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
