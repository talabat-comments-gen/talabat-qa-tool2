import streamlit as st
import os
import time
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Talabat Final Engine", layout="centered")
st.title("🚀 Talabat Final Engine")

# 2. إعدادات الـ API
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# 3. واجهة المستخدم
chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Final Log"):
    if chat_input:
        # عد تنازلي
        with st.empty():
            for seconds in range(3, 0, -1):
                st.info(f"Analyzing data... {seconds}")
                time.sleep(1)
            st.empty()

        # معالجة البيانات
        with st.spinner('Extracting...'):
            try:
                system_prompt = """
                You are a technical data extraction engine. 
                Output ONLY the data in this exact schema. 
                NO conversational sentences, NO apologies, NO intros.

                Format:
                [CST Request] // [Issue Type] // [Details] // [Action/Result] // [Order ID] // [CST Info]

                Rules:
                1. Extract Order ID from the chat. If NOT found, write 'N/A'.
                2. Use '//' as the separator.
                3. Keep descriptions extremely short (shorthand/bullet-style).
                4. If the agent claims system limitation, mention 'System limitation'.
                5. If CST info is missing, write 'N/A'.
                6. Ignore all pleasantries, greetings, and apologies.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # عرض النتيجة
                st.text_area("Final Log:", value=chat_completion.choices[0].message.content, height=150)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
