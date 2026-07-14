import streamlit as st
from groq import Groq

st.set_page_config(page_title="Talabat QA Engine", layout="centered")
st.title("🚀 Talabat QA Analysis Engine")

# كشف الأعطال في السيكريتس
try:
    api_key = st.secrets["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"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"System Error: {e}")
    st.warning(f"The system currently sees these keys in your Secrets: {list(st.secrets.keys())}")
    st.stop()

# Text area
chat_input = st.text_area("Paste Chat Transcript Here:", height=400)

if st.button("Generate Analysis"):
    if chat_input:
        with st.spinner('Analyzing with Groq...'):
            try:
                prompt = f"""
                You are the Talabat Log Engine. Extract FACTS ONLY from the chat transcript.
                Strictly follow this structure:
                --- LOG ---
                (CST: , RST: , Agent: , RNA: , FU: )
                --- CASE SUMMARY ---
                (Customer Issue, Action Taken, Final Result)
                
                Chat: {chat_input}
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-70b-8192",
                    temperature=0.3
                )
                
                st.success("Analysis Complete!")
                st.markdown("### 📝 Result:")
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
