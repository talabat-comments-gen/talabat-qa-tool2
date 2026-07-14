import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Raw Log", layout="centered")
st.title("🚀 Talabat Raw Log (Just Facts)")

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
                [Issue] // [Details (Include 2% direct quote from chat)] // [Action (Include 2% direct quote from chat)] // [Order ID]

                Rules:
                1. 100% Accuracy: Use the chat's actual words. Do not interpret.
                2. [Issue]: Short category (e.g., 'Missing food').
                3. [Details]: Describe what happened, plus a short phrase from the chat in quotes (e.g., 'Ordered 8 received 4: "جالي نقص"').
                4. [Action]: Quote the agent's actual words (e.g., 'Agent: "مش هقدر اخذ اي اجراء"').
                5. [Order ID]: Only long numerical ID. If not found, 'N/A'.
                6. NO headers, NO labels, NO 'Denied' or 'Resolution' status, NO names.
                7. Just the data string.
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
