import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v25", layout="centered", page_icon="🚀")

# State Management
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "voted" not in st.session_state: st.session_state.voted = False

st.title("🚀 Surgical Pro v25")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Input Section
chat_input = st.text_area("Paste chat transcript:", height=150)
contact_drive = st.text_input("Contact Drive (Core Identity):")

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
            The CONTACT DRIVE is the core backbone of this case. 
            Ignore generic categories. Only focus on the drive provided.
            
            Format strictly using tags [OPTION_A], [OPTION_B], [OPTION_C], [OPTION_D].
            Inside each tag, output:
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action]
            
            RULES:
            - NO Order ID.
            - NO UNCLEAR.
            - NO ARABIC.
            - Use abbreviations.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                model="llama-3.3-70b-versatile", temperature=0.0
            )
            st.session_state.raw_response = response.choices[0].message.content

# 2. Advanced Parsing & Professional UI
if "raw_response" in st.session_state:
    raw = st.session_state.raw_response
    
    # Regex splitting to fix the mismatch error once and for all
    # بتقسم النص بناءً على الـ tags مهما كان اللي مكتوب قبلهم
    parts = re.split(r'\[OPTION_[A-D]\]', raw)
    # بنشيل أي عنصر فاضي
    options = [p.strip() for p in parts if p.strip()]

    if len(options) < 4:
        st.error("AI output format is inconsistent. Showing raw output:")
        st.code(raw)
    else:
        if not st.session_state.voted:
            # عرض كل خيار في "مستطيل" احترافي
            for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
                with st.container(border=True):
                    st.subheader(f"Option {opt_label}")
                    st.code(options[i], language=None)
                    if st.button(f"✅ Select & Train {opt_label}", key=f"btn_{opt_label}"):
                        st.session_state.selected_result = options[i]
                        st.session_state.golden_examples.append(options[i])
                        st.session_state.voted = True
                        st.rerun()
        else:
            st.success("🎉 Thanks for your feedback! The model has been trained.")
            if st.button("🔄 Reset"):
                st.session_state.voted = False
                st.rerun()

# 3. Final Display
if st.session_state.voted:
    st.divider()
    st.subheader("Selected Report")
    with st.container(border=True):
        st.code(st.session_state.selected_result, language=None)
