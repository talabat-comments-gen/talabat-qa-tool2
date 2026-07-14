import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

# 2. Comprehensive Drive Map
DRIVE_MAP = [
    "Complaint about late order", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Missing item / Wrong item", "Delivery area/fee inquiry",
    "Negative", "Positive", "Order tracking issue"
]

# 3. UI
st.title("🍔 Talabat Log Tool (Concise)")
st.markdown("---")

chat_input = st.text_area("Paste Transcript / Details:", height=150)
selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_MAP)

if st.button("🚀 Generate Pro Log"):
    if chat_input:
        with st.spinner('Writing log...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            # البرومبت الجديد: صارم جداً ومختصر
            prompt = f"""
            You are a professional Talabat agent. Analyze the transcript for: {selected_drive}.
            
            Generate a log in this exact format:
            [Issue Context] // [Action 1] // [Action 2] // [Resolution/Compensation] // [Outcome]
            
            RULES:
            1. Use abbreviations (CST, RST, comp, OT, cst info).
            2. NO greetings, NO endings, NO survey mentions, NO "Dear customer" fluff.
            3. Be factual, technical, and concise.
            4. Follow the slash-separated pattern strictly.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.2
                )
                log_result = response.choices[0].message.content
                st.session_state.log_result = log_result
            except Exception as e:
                st.error(f"Error: {e}")

# 4. Display
if "log_result" in st.session_state and st.session_state.log_result:
    st.code(st.session_state.log_result, language=None)
    if st.button("🔄 Reset"):
        st.session_state.log_result = ""
        st.rerun()
