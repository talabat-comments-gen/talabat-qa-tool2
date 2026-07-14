import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat QA Engine", layout="centered")
st.title("🚀 Talabat QA Analysis Engine")

# قراءة المفتاح
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

if st.button("Generate Analysis"):
    if chat_input:
        with st.spinner('Analyzing...'):
            try:
                # استخدام الموديل المحدث
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Analyze this: {chat_input}"}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3
                )
                st.success("Analysis Complete!")
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
