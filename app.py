import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

# 2. Comprehensive Drive Map
DRIVE_MAP = [
    "Complaint about short delay (0-10 mins)", "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)", "Complaint about extreme delay (+30 mins)",
    "Follow up on existing case", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Missing item", "Wrong item", "Spilled food",
    "Delivery area/fee inquiry", "Negative feedback", "Positive feedback", 
    "Order tracking issue", "Payment method inquiry", "Rider related inquiry"
]

# 3. UI
st.title("🍔 Talabat Log Tool (The Concise Way)")
st.markdown("---")

chat_input = st.text_area("Paste Transcript / Details:", height=150)
selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_MAP)

if st.button("🚀 Generate Concise Log"):
    if chat_input:
        with st.spinner('Writing log...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            # البرومبت ده صارم: (Context // Action // Action // Resolution // Outcome)
            prompt = f"""
            You are a professional Talabat agent. Analyze the transcript for: {selected_drive}.
            
            Generate a log in this exact strict format:
            [Issue/Context] // [Action 1] // [Action 2] // [Resolution/Comp] // [Outcome/Status]
            
            RULES:
            1. NO greetings, NO endings, NO survey mentions, NO "Dear customer".
            2. Use technical abbreviations (CST, RST, comp, OT, TGO, TMP).
            3. Be factual and extremely concise.
            4. If no compensation was given, skip the comp part.
            5. Follow the slash-separated pattern strictly.
            6. No Arabic words, use English only.
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
