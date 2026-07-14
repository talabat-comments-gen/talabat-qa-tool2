import streamlit as st
import os
import re
from groq import Groq

# 1. Config & UI Styling
st.set_page_config(page_title="Surgical Pro | Professional AI", layout="centered", page_icon="⚡")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    div[data-testid="stCodeBlock"] { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "voted" not in st.session_state: st.session_state.voted = False
if "raw_response" not in st.session_state: st.session_state.raw_response = None
if "selected_result" not in st.session_state: st.session_state.selected_result = ""

# 3. Header
st.title("⚡ Surgical Pro v27")
st.markdown("### Professional Contact Analysis Suite")
st.markdown("---")

# API Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 4. Input Section
with st.container():
    chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
    contact_drive = st.text_input("Contact Drive (The Backbone of this case):", placeholder="e.g., Cooking Instruction")

if st.button("🚀 Analyze & Generate Variants", type="primary"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Performing deep analysis...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            
            Memory: {memory_str}
            CONTACT DRIVE: {contact_drive if contact_drive else "General Inquiry"}
            
            CORE INSTRUCTION: 
            The CONTACT DRIVE is the core backbone and identity of the case. 
            All [Issue] classifications MUST stem directly from this drive. 
            Ignore all generic tags.
            
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
                # Using 8b-instant for zero Rate Limits and ultra-fast speed
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", 
                    temperature=0.0
                )
                st.session_state.raw_response = response.choices[0].message.content
            except Exception as e:
                st.error(f"❌ Connection Error: {str(e)}")

# 5. Parsing & UI Display
if st.session_state.raw_response:
    raw = st.session_state.raw_response
    parts = re.split(r'\[OPTION_[A-D]\]', raw)
    options = [p.strip() for p in parts if p.strip()]

    if len(options) < 4:
        st.warning("AI output format is adjusting... showing raw result:")
        st.code(raw)
    else:
        if not st.session_state.voted:
            st.markdown("### Select the best variation:")
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
            st.success("🎉 Case successfully processed and learned!")
            if st.button("🔄 Start New Case"):
                st.session_state.voted = False
                st.session_state.raw_response = None
                st.rerun()

# 6. Final Result
if st.session_state.voted:
    st.divider()
    st.markdown("### ✅ Final Report")
    with st.container(border=True):
        st.code(st.session_state.selected_result, language=None)
