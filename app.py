import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (Agent Mode)")

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
        with st.spinner('Summarizing...'):
            try:
                # الـ Prompt ده هيخليه يكتب بلسانك أنت (بصيغة المتكلم)
                system_prompt = """
                You are the agent. Write a summary of the chat as if YOU are the agent (use 'I').
                Combine all actions into one single, short paragraph.
                DO NOT repeat 'CST' or 'Agent' for every line.
                Format: 
                CST: [Issue] // Agent: [I did X, Y, Z, then ended chat nicely]
                
                Rules:
                1. Always use 'I' when talking about agent actions.
                2. If the conversation finished, end with 'ended chat nicely'.
                3. Keep it professional and very short.
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
