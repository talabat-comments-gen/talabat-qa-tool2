import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Final Engine", layout="centered")
st.title("🚀 Talabat Data Logger (v3)")

# 2. API Key setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# 3. Input UI
chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Final Log"):
    if chat_input:
        with st.spinner('Extracting details...'):
            try:
                system_prompt = """
                You are a data logger. Extract facts ONLY.
                
                Format:
                [CST Request] // [Detailed Issue] // [Agent Action] // [Resolution] // [Order ID] // [CST Name]

                Rules:
                1. [Detailed Issue]: Explain the problem in detail (e.g., "Ordered 8 Shawerma, only received 4").
                2. [Agent Action]: Use short, fixed phrases only. DO NOT explain. Examples: 'can't take any action', 'checked order', 'processed refund', 'escalated to team'.
                3. [Resolution]: One or two words only. Examples: 'Denied', 'Resolved', 'Pending'.
                4. [Order ID]: Extract ONLY the numerical order ID. If not found, write 'N/A'.
                5. [CST Name]: Extract the customer name.
                6. STRICT: NO greetings, NO apologies, NO filler. Use '//' as separator.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # 4. Result Display
                st.text_area("Final Log:", value=chat_completion.choices[0].message.content, height=150)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
