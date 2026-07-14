import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Surgical Pro v14", layout="wide")

# 1. Memory Store
if "golden_examples" not in st.session_state:
    st.session_state.golden_examples = []

st.title("🚀 Surgical Pro v14 (Voting Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat here:", height=150)

if st.button("Generate Options"):
    if chat_input:
        # Inject memory into the prompt so it learns from your votes
        memory_str = "\n".join(st.session_state.golden_examples)
        
        system_prompt = f"""
        You are a Senior Talabat Agent. Generate TWO distinct versions of the report.
        
        Golden Examples (Adopt this style for future generations):
        {memory_str}
        
        Format Requirement:
        VERSION 1:
        [SUMMARY]: ...
        [DATA]: [Issue] // [Details] // [Action] // [Order ID]
        [UNCLEAR]: ...
        
        VERSION 2 (Alternative phrasing):
        [SUMMARY]: ...
        [DATA]: [Issue] // [Details] // [Action] // [Order ID]
        [UNCLEAR]: ...
        
        Use Abbreviations (CST, RST, RNA, NAT). NO ARABIC.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
            model="llama-3.3-70b-versatile", temperature=0.0
        )
        st.session_state.raw_result = response.choices[0].message.content

# 2. Display Options & Voting
if "raw_result" in st.session_state:
    raw = st.session_state.raw_result
    
    # Simple Parsing
    try:
        ver1 = raw.split("VERSION 2:")[0].replace("VERSION 1:", "").strip()
        ver2 = raw.split("VERSION 2:")[1].strip()
    except:
        ver1 = raw
        ver2 = "Error generating second version."

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option A")
        st.code(ver1, language=None)
        if st.button("✅ Vote & Train (Option A)"):
            st.session_state.golden_examples.append(ver1)
            st.success("Trained on A!")
            
    with col2:
        st.subheader("Option B")
        st.code(ver2, language=None)
        if st.button("✅ Vote & Train (Option B)"):
            st.session_state.golden_examples.append(ver2)
            st.success("Trained on B!")
