import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Final Engine", layout="centered")
st.title("🚀 Talabat Data Logger")

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
                # الـ Prompt الجديد اللي بيجبره يشرح المشكلة ويدور على رقم الطلب الصح
                system_prompt = """
                You are a Technical Support Analyst. Extract case data from the transcript.

                Format:
                [CST Request] // [Detailed Issue] // [Agent Action] // [Resolution] // [Order ID] // [CST Name]

                Rules:
                1. [Detailed Issue]: Explain the problem in detail (e.g., "Customer ordered 8 Shawerma, only received 4"). DO NOT summarize into vague terms like "Missing items".
                2. [Order ID]: Extract ONLY the numerical order ID (the long number). IGNORE Chat Ticket IDs or any other IDs. If no Order ID is found, write 'N/A'.
                3. [Resolution]: State exactly what happened (e.g., "Denied - System limitation", "Refund issued").
                4. [CST Name]: Write the customer name found in the chat.
                5. STRICT: NO greetings, NO apologies, NO filler. Output ONLY the schema above.
                6. Use '//' as the separator.
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
