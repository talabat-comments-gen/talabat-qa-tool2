import streamlit as st
import os
import re
import groq
from groq import Groq

# 1. Config & Page Setup
st.set_page_config(page_title="Surgical Pro v26", layout="centered", page_icon="🚀")

# 2. State Management
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "voted" not in st.session_state: st.session_state.voted = False
if "raw_response" not in st.session_state: st.session_state.raw_response = None
if "selected_result" not in st.session_state: st.session_state.selected_result = ""

st.title("🚀 Surgical Pro v26")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 3. Input Section
chat_input = st.text_area("Paste chat transcript:", height=150)
contact_drive = st.text_input("Contact Drive (Core Identity of the case):")

if st.button("Generate Variations"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Analyzing...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            
            Memory: {memory_str}
            CONTACT DRIVE: {contact_drive if contact_drive else "General Inquiry"}
            
            CORE INSTRUCTION: 
            The CONTACT DRIVE is the most important element of this report. 
            It is the backbone and core identity of the case. 
            Ignore generic categories; use the Contact Drive to define the [Issue].
            
            Format strictly using tags [OPTION_A], [OPTION_B], [OPTION_C], [OPTION_D].
            Inside each tag, output:
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action]
            
            STRICT RULES:
            - NO Order ID.
            - NO UNCLEAR section.
            - NO ARABIC.
            - Use abbreviations (CST, RST, RNA).
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.3-70b-versatile", 
                    temperature=0.0
                )
                st.session_state.raw_response = response.choices[0].message.content
            except groq.RateLimitError:
                st.error("⚠️ Rate Limit Hit! الـ API تعب. استنى 30 ثانية وجرب تاني.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# 4. Professional Parsing & UI Display
if st.session_state.raw_response:
    raw = st.session_state.raw_response
    
    # Regex splitting (Robust Parsing)
    parts = re.split(r'\[OPTION_[A-D]\]', raw)
    options = [p.strip() for p in parts if p.strip()]

    if len(options) < 4:
        st.error("AI output format mismatch. Raw output below:")
        st.code(raw)
    else:
        if not st.session_state.voted:
            for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
                with st.container(border=True):
                    st.subheader(f"Option {opt_label}")
                    st.code(options[i], language=None)
                    if st.button(f"✅ Vote & Select {opt_label}", key=f"btn_{opt_label}"):
                        st.session_state.selected_result = options[i]
                        st.session_state.golden_examples.append(options[i])
                        st.session_state.voted = True
                        st.rerun()
        else:
            st.success("🎉 Thanks for your feedback! The model has been trained.")
            if st.button("🔄 Reset & New Case"):
                st.session_state.voted = False
                st.session_state.raw_response = None
                st.rerun()

# 5. Final Display
if st.session_state.voted:
    st.divider()
    st.subheader("Final Selected Report")
    with st.container(border=True):
        st.code(st.session_state.selected_result, language=None)
