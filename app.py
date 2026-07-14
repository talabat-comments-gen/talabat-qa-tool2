import streamlit as st
from groq import Groq

st.set_page_config(page_title="Talabat QA Engine", layout="centered")
st.title("🚀 Talabat QA Analysis Engine")

# التعديل هنا: محاولة القراءة بطريقة أكثر مرونة
api_key = st.secrets.get("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")

if not api_key:
    st.error("Error: GROQ_API_KEY is not found. Please check your Secrets configuration again.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# Text area
chat_input = st.text_area("Paste Chat Transcript Here:", height=400)

if st.button("Generate Analysis"):
    if chat_input:
        with st.spinner('Analyzing...'):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Analyze this: {chat_input}"}],
                    model="llama3-70b-8192",
                    temperature=0.3
                )
                st.success("Analysis Complete!")
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
