import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Dashboard", layout="centered")
st.title("🚀 Talabat Multi-Issue Dashboard")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Extract Data"):
    if chat_input:
        with st.spinner('Parsing into bars...'):
            try:
                system_prompt = """
                You are a data extraction engine. 
                - Analyze the chat transcript completely.
                - Identify EACH distinct complaint or issue.
                - For EACH issue, output a NEW LINE.
                - Format each line exactly: [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                1. STRICTLY ENGLISH ONLY. ABSOLUTELY NO ARABIC CHARACTERS.
                2. [Order ID]: ONLY NUMERIC. If ID has letters/dashes, write 'N/A'.
                3. Sort by importance.
                4. NO intros, NO titles, NO headers, NO filler. ONLY the data lines.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # معالجة النتيجة وعرضها في بارات
                raw_data = chat_completion.choices[0].message.content
                lines = raw_data.strip().split('\n')
                
                st.subheader("Extracted Issues:")
                for line in lines:
                    if line.strip(): # يتأكد إن السطر مش فاضي
                        st.info(line.strip()) # بيعرض كل واحدة في بار منفصل
                
            except Exception as e:
                st.error(f"Error: {e}")
