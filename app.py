import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat comment generator", layout="centered")
st.title("🚀 Talabat comment generator (Strict Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste chat here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.empty():
            for seconds in range(3, 0, -1):
                st.info(f"Extracting Data... {seconds}")
                time.sleep(1)
            st.empty()

        with st.spinner('Processing...'):
            try:
                # الـ Prompt ده "مقفول" على 4 سطور، ممنوع الجمل، وممنوع الـ "I"
                system_prompt = """
                You are a Data Entry Clerk. Extract info into 4 lines ONLY. 
                NO full sentences. Use bullet-style shorthand.
                
                Format:
                CST: [Item issue / Problem]
                Agent: [Action 1, Action 2]
                Notes: [Key facts / Details]
                Status: ended chat since customer not responding
                
                Rules:
                1. NO "I", NO politeness, NO fluff.
                2. If no details, write N/A.
                3. Use simple, direct keywords.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.text_area("Final Log:", value=chat_completion.choices[0].message.content, height=200)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
