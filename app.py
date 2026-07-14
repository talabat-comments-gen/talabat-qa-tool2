import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Final Engine", layout="centered")
st.title("🚀 Talabat Raw Log (Strict ID)")

# 2. API Key setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        try:
            # الـ Prompt ده "حجر" على أي رقم فيه شرطات
            system_prompt = """
            You are a data extraction engine. Output facts ONLY.
            
            Format:
            [Issue] // [Details] // [Action] // [Order ID]
            
            Rules:
            1. [Issue]: Short category (e.g., 'Missing food').
            2. [Details]: Description + 2% quote (e.g., 'Ordered 8 received 4: "جالي نقص"').
            3. [Action]: Agent quote (e.g., 'Agent: "مش هقدر اخذ اي اجراء"').
            4. [Order ID]: STRICTLY NUMERIC DIGITS ONLY.
               - IF THE ID CONTAINS HYPHENS (-), DASHES, OR LETTERS: IGNORE IT COMPLETELY AND WRITE 'N/A'.
               - Do not output the Ticket ID or Chat ID.
            5. NO names, NO headers, NO filler. JUST the data string.
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
