import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v18", layout="centered")

# State Management
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "selected_result" not in st.session_state: st.session_state.selected_result = ""
if "voted" not in st.session_state: st.session_state.voted = False

st.title("🚀 Surgical Pro v18")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Input Section
chat_input = st.text_area("Paste chat transcript:", height=150)
custom_notes = st.text_input("Additional Instructions:", placeholder="e.g., Focus on refund policy...")

if st.button("Generate 4 Variations"):
    if chat_input:
        st.session_state.voted = False # Reset state when generating new options
        with st.spinner('Analyzing...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            context_block = f"Additional Context: {custom_notes}" if custom_notes else ""
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            Memory (Use this style): {memory_str}
            {context_block}
            
            Format for each:
            [OPTION_X]
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action] // [Order ID]
            
            STRICT RULES: NO UNCLEAR section. NO ARABIC. Use abbreviations.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                model="llama-3.3-70b-versatile", temperature=0.0
            )
            st.session_state.raw_response = response.choices[0].message.content

# 2. Display & Selection
if "raw_response" in st.session_state:
    raw = st.session_state.raw_response
    
    options = {"A": "", "B": "", "C": "", "D": ""}
    for opt in ["A", "B", "C", "D"]:
        try:
            part = raw.split(f"[OPTION_{opt}]")[1].split("[OPTION_")[0]
            options[opt] = part.strip()
        except:
            options[opt] = "Error generating."

    # Logic: Show options OR Thanks message
    if not st.session_state.voted:
        for opt, content in options.items():
            st.subheader(f"Option {opt}")
            st.code(content, language=None)
            
            if st.button(f"✅ Vote & Select Option {opt}"):
                st.session_state.selected_result = content
                st.session_state.golden_examples.append(content)
                st.session_state.voted = True
                st.rerun()
    else:
        st.success("🎉 Thanks for your feedback! The AI has been trained on your choice.")
        if st.button("🔄 Reset & Generate New"):
            st.session_state.voted = False
            st.rerun()

# 3. Final Selected Area
if st.session_state.selected_result and st.session_state.voted:
    st.divider()
    st.subheader("Final Selected Report")
    st.code(st.session_state.selected_result, language=None)
