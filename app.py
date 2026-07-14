import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v15", layout="wide")

# Session State for Memory
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "option_a" not in st.session_state: st.session_state.option_a = ""
if "option_b" not in st.session_state: st.session_state.option_b = ""
if "displayed_content" not in st.session_state: st.session_state.displayed_content = ""

st.title("🚀 Surgical Pro v15 (Control Center)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 2. Main Input
chat_input = st.text_area("Paste chat transcript:", height=150)

if st.button("Generate Options"):
    if chat_input:
        with st.spinner('Generating smart alternatives...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate TWO versions of the report.
            
            Memory (Use this style): {memory_str}
            
            Rules:
            1. Output EXACTLY as follows:
            [OPTION_A]
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action] // [Order ID]
            [UNCLEAR]: ...
            
            [OPTION_B]
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action] // [Order ID]
            [UNCLEAR]: ...
            
            2. NO ARABIC. Use abbreviations.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                model="llama-3.3-70b-versatile", temperature=0.0
            )
            raw = response.choices[0].message.content
            
            # Smart Parsing
            try:
                st.session_state.option_a = raw.split("[OPTION_A]")[1].split("[OPTION_B]")[0].strip()
                st.session_state.option_b = raw.split("[OPTION_B]")[1].strip()
                st.success("Options Generated! Use the Sidebar to choose.")
            except:
                st.error("Parsing failed. Showing raw output:")
                st.code(raw)

# 3. Sidebar Control Center
with st.sidebar:
    st.header("🎛️ Command Center")
    if st.session_state.option_a:
        if st.button("👈 Show Option A & Train"):
            st.session_state.displayed_content = st.session_state.option_a
            st.session_state.golden_examples.append(st.session_state.option_a)
            st.toast("Trained on A!")
            
        if st.button("👉 Show Option B & Train"):
            st.session_state.displayed_content = st.session_state.option_b
            st.session_state.golden_examples.append(st.session_state.option_b)
            st.toast("Trained on B!")
    else:
        st.info("Generate options to see controls.")

# 4. Display Area
if st.session_state.displayed_content:
    st.subheader("Selected Result")
    st.code(st.session_state.displayed_content, language=None)
