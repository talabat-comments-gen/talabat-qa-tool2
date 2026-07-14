import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Final Engine", layout="centered")
st.title("🚀 Talabat Multi-Bar Engine")

# إعداد الـ API
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate & Extract"):
    if chat_input:
        with st.spinner('Analyzing & Translating...'):
            try:
                system_prompt = """
                You are a professional data extraction and translation engine.
                1. Read the entire chat transcript.
                2. Extract all distinct issues.
                3. Translate all content from Arabic to English ACCURATELY and LITERALLY. Do not summarize or change meaning.
                4. Output each issue as a SEPARATE line.
                5. Format: [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - STRICTLY ENGLISH ONLY. NO ARABIC CHARACTERS ALLOWED IN OUTPUT.
                - If the Order ID contains letters, dashes, or special characters, write 'N/A'.
                - Sort by importance.
                - NO headers, NO titles, NO conversation. Just the formatted strings.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # معالجة النتائج وعرضها
                raw_output = chat_completion.choices[0].message.content
                lines = [line.strip() for line in raw_output.split('\n') if line.strip()]
                
                for index, line in enumerate(lines):
                    # استخدام st.code عشان يظهر زر الـ Copy تلقائياً
                    st.code(line, language=None)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
