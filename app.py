import streamlit as st
import os
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Surgical Pro - Final", layout="centered")

# 2. Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

st.title("🚀 Talabat Surgical Pro (Stable)")

if not api_key:
    st.error("API Key not found! Please check your Streamlit secrets or environment variables.")
else:
    client = Groq(api_key=api_key)

    chat_input = st.text_area("Paste chat transcript here:", height=200)

    if st.button("Generate"):
        if not chat_input:
            st.warning("Please paste the chat.")
        else:
            with st.spinner('Thinking...'):
                try:
                    # الـ Prompt المباشر
                    system_prompt = """
                    You are a Senior Talabat Agent. 
                    Format:
                    [SUMMARY]: Single professional sentence.
                    [DATA]: Line format [Issue] // [Details] // [Action] // [Order ID]
                    [UNCLEAR]: Any missing info.
                    Use abbreviations (CST, RST, RNA). NO ARABIC.
                    """

                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Transcript: {chat_input}"}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.0
                    )
                    
                    raw_output = chat_completion.choices[0].message.content
                    
                    # دي أهم حتة: هنعرض الـ Raw Output عشان لو التقطيع فشل، نشوف بعنينا الـ AI كتب إيه
                    st.subheader("Raw Output (For Debugging)")
                    st.code(raw_output)

                    # محاولة التقطيع الذكي
                    if "[SUMMARY]:" in raw_output:
                        st.subheader("Parsed Report")
                        # (ممكن تضيف هنا كود التقطيع براحتك، بس دلوقتى أنت شايف الـ raw output)
                        
                except Exception as e:
                    st.error(f"Error occurred: {e}")
