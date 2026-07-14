import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Raw Logger", layout="centered")
st.title("🚀 Talabat Event Logger")

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
        with st.spinner('Logging events...'):
            try:
                # الـ Prompt ده ممنوع فيه التفكير، ممنوع فيه الحالة، وممنوع فيه الرغي
                system_prompt = """
                You are a pure event logger. 
                1. Strip ALL apologies, greetings, thanks, and polite fluff.
                2. DO NOT write any 'Status', 'Outcome', or 'Resolution'. 
                3. DO NOT interpret. ONLY state what the Customer asked and what the Agent did.
                4. Use bullet points.
                
                Format:
                Customer: [Core request or action]
                Agent: [Action taken]
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.text_area("Event Log:", value=chat_completion.choices[0].message.content, height=250)
                
            except Exception as e:
                st.error(f"Groq Error: {e}")
    else:
        st.warning("Paste the chat first.")
