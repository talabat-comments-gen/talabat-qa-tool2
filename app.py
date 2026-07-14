import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Raw Log", layout="centered")
st.title("🚀 Talabat English-Only Log")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Extracting data...'):
            try:
                system_prompt = """
                You are a data extraction engine. 
                STRICT LANGUAGE RULE: Output MUST be in ENGLISH ONLY. 
                ABSOLUTELY NO ARABIC CHARACTERS ALLOWED in the result.

                Format:
                [Issue] // [Details] // [Action] // [Order ID]

                Rules:
                1. [Issue]: Category (e.g., Missing items).
                2. [Details]: English summary of the issue (e.g., Ordered 8 received 4). 
                3. [Action]: English summary of the agent's action (e.g., Agent denied request).
                4. [Order ID]: STRICTLY NUMERIC DIGITS ONLY.
                   - IF THE ID CONTAINS HYPHENS (-), DASHES, OR LETTERS: IGNORE IT AND WRITE 'N/A'.
                5. NO names, NO headers, NO filler, NO Arabic. Output ONLY the data string.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.text_area("Data String:", value=chat_completion.choices[0].message.content, height=100)
                
            except Exception as e:
                st.error(f"Error: {e}")
