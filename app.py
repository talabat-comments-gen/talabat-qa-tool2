import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (English)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# الشات بار أصغر (200)
chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        # عد تنازلي 3 ثواني
        with st.empty():
            for seconds in range(3, 0, -1):
                st.info(f"Analyzing in {seconds} seconds...")
                time.sleep(1)
            st.empty()

        with st.spinner('Generating...'):
            try:
                # الـ Prompt الجديد (إنجليزي فقط ومختصر)
                system_prompt = """
                You are a data scribe. 
                1. Extract the issue using the CUSTOMER'S EXACT WORDS. 
                2. Agent actions: Use clipped shorthand ONLY (e.g., 'asked for photo', 'checked order', 'informed finance'). NO 'I'.
                3. Format strictly: CST: [Exact Issue] // Agent: [Actions] // Status: [Final State]
                4. If customer stops responding, write: 'ended chat since customer not responding'.
                5. NO politeness, NO fluff, NO full sentences. Extremely concise.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # الكومنت بار أطول (250)
                st.text_area("Final Log:", value=chat_completion.choices[0].message.content, height=250)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
