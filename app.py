import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (Strict Extraction)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste Chat Transcript Here:", height=400)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Extracting...'):
            try:
                # الـ Prompt ده هيجبره يلتزم بكلمات العميل ويختصر أفعالك
                system_prompt = """
                You are a data scribe. 
                1. Extract the issue using the CUSTOMER'S EXACT WORDS (e.g., if they say 'spilled', write 'spilled'). DO NOT generalize.
                2. Agent actions: Use clipped shorthand ONLY (e.g., 'asked for photo', 'checked order', 'informed finance').
                3. Format: CST: [Exact Issue] // Agent: [Actions] // Status: [Final State]
                4. If customer stops responding, end with: 'ended chat since customer not responding'.
                5. NO politeness, NO 'I', NO fluff. Be extremely concise.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.code(chat_completion.choices[0].message.content, language=None)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
