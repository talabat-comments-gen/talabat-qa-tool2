import streamlit as st
import os
from groq import Groq

# (API setup remains the same)
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Log"):
    if chat_input:
        try:
            # الـ Prompt المحدث بقواعد صارمة للـ ID
            system_prompt = """
            You are a data extraction engine. Output facts ONLY.
            
            Format:
            [Issue] // [Details] // [Action] // [Resolution] // [Order ID]
            
            Rules:
            1. [Issue]: Category (e.g., 'Missing food').
            2. [Details]: Summary (e.g., 'Ordered 8, received 4').
            3. [Action]: Fixed phrases (e.g., 'can't take any action', 'checked order').
            4. [Resolution]: One or two words (e.g., 'Denied', 'Resolved').
            5. [Order ID]: STRICT RULE: Must be purely numeric (digits only). 
               - If the ID contains letters, dashes, or special characters (like a Chat Ticket ID), IGNORE IT completely and write 'N/A'.
            6. NO names, NO headers, NO filler. Output ONLY the data string.
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
