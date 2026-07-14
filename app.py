import streamlit as st
import os
import time
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine (Strict Data)")

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
                st.info(f"Analyzing... {seconds}")
                time.sleep(1)
            st.empty()

        with st.spinner('Extracting facts...'):
            try:
                # الـ Prompt ده "بيعمل بلوك" لأي اعتذار أو مجاملة
                system_prompt = """
                You are a data logger. Extract ONLY the functional facts.
                
                STRICT RULES:
                1. IGNORE all apologies, thank yous, and pleasantries from both CST and Agent.
                2. Write ONLY the problem and the operational action.
                3. If the agent apologized, IGNORE it. Write the step taken (e.g., 'Checked order', 'Escalated to finance').
                4. No full sentences. Use shorthand.
                
                Format:
                CST: [Problem]
                Agent: [Action taken]
                Notes: [Specifics: missing items, order details, etc.]
                Status: ended chat since customer not responding
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
