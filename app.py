import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v13", layout="centered")

# 2. Session Memory (Training Data)
if "golden_examples" not in st.session_state:
    st.session_state.golden_examples = []

st.title("🚀 Surgical Pro v13 (Learning Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat here:", height=150)

if st.button("Generate & Process"):
    if chat_input:
        # Load Memory for Prompt Injection
        memory_str = "\n".join(st.session_state.golden_examples)
        
        system_prompt = f"""
        You are a Senior Talabat Agent.
        
        GOLDEN STANDARDS (Examples you must follow):
        {memory_str}
        
        Format:
        [SUMMARY]: One sharp sentence.
        [DATA]: Line format [Issue] // [Details] // [Action] // [Order ID]
        [UNCLEAR]: Any missing info.
        
        RULES: NO ARABIC. Use abbreviations.
        """

        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
            model="llama-3.3-70b-versatile", temperature=0.0
        )
        st.session_state.raw_result = response.choices[0].message.content

# 3. Display & Training Section
if "raw_result" in st.session_state:
    st.divider()
    st.subheader("Result:")
    
    # Display result in an editable text area so you can fix it yourself
    edited_result = st.text_area("You can fix the result here:", value=st.session_state.raw_result, height=200)
    
    # Training Button
    if st.button("✅ Save as Golden Standard (Train AI)"):
        st.session_state.golden_examples.append(edited_result)
        st.success("Trained! The AI will use this style for next outputs.")
        st.info(f"Total training examples: {len(st.session_state.golden_examples)}")
