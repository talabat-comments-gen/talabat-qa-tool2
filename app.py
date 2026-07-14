import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Pure Logger", layout="centered")
st.title("🚀 Talabat Pure Logger (Accuracy 100%)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Extracting...'):
            try:
                system_prompt = """
                You are a data extraction engine. Output facts ONLY.
                
                Format (Strictly this order):
                [Issue] // [Details] // [Action] // [Resolution] // [Order ID]

                Rules:
                1. 100% Factual Accuracy: Only extract what is clearly in the text.
                2. NO names, NO personal identifiers, NO agent/customer names.
                3. [Issue]: Short category (e.g., 'Missing food', 'Late delivery').
                4. [Details]: Summary of what happened (e.g., 'Ordered 8, received 4').
                5. [Action]: Fixed phrases only (e.g., 'can't take any action', 'checked order').
                6. [Resolution]: One or two words (e.g., 'Denied', 'Resolved').
                7. [Order ID]: Only long numerical ID. If not found, 'N/A'.
                8. NO headers, NO labels in output, JUST the data string.
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
    else:
        st.warning("Please paste the chat transcript first.")
