import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="wide")

# 2. Master Contact Drives List (Comprehensive)
DRIVE_LIST = [
    "Complaint about short delay (0-10 mins)",
    "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)",
    "Complaint about extreme delay (+30 mins)",
    "Order cancellation / Refund request",
    "Missing item / Wrong item / Spilled food",
    "Food quality / Temperature / Allergens",
    "Check order status / Tracking issue",
    "Payment method / Double charge / Wallet",
    "Partner related inquiry (Menu, availability)",
    "Rider related inquiry (Behavior, contact)",
    "Delivery area / Fee inquiry",
    "Invoice / VAT / Receipt issues",
    "Account / Subscription / Loyalty / Rewards",
    "Technical issue (App/Website)",
    "Contactless delivery inquiry",
    "Follow up on existing case",
    "Positive feedback",
    "Negative feedback"
]

# 3. UI
st.title("🍔 Talabat Log Tool (Master Version)")
st.markdown("---")

col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    chat_input = st.text_area("Paste Chat Transcript:", height=150)
with col_input2:
    selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_LIST)

if st.button("🚀 Generate Comment"):
    if chat_input:
        with st.spinner('Generating...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are a strict Talabat Log Generator. Analyze the transcript for: {selected_drive}.
            
            OUTPUT FORMAT (FOLLOW EXACTLY):
            SUMMARY: [One single sentence summary of the issue]
            COMMENT: [Issue/Context] // [Action 1] // [Action 2] // [Resolution/Comp] // [Outcome]
            
            RULES:
            1. No greetings, no endings, no survey mentions, no "Dear customer", no filler.
            2. Strict format for COMMENT: [Issue] // [Action] // [Action] // [Res] // [Outcome].
            3. Use technical abbreviations (CST, RST, OT, comp, cst info).
            4. No Arabic in the output (English only).
            5. If no compensation, end after Resolution.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.1
                )
                output = response.choices[0].message.content
                
                sum_match = re.search(r'SUMMARY:(.*?)(?=COMMENT:)', output, re.DOTALL | re.IGNORECASE)
                com_match = re.search(r'COMMENT:(.*)', output, re.DOTALL | re.IGNORECASE)
                
                st.session_state.summary = sum_match.group(1).strip() if sum_match else "Could not extract Summary."
                st.session_state.comment = com_match.group(1).strip() if com_match else output
            except Exception as e:
                st.error(f"Error: {e}")

if "summary" in st.session_state:
    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.subheader("📋 Summary")
        st.info(st.session_state.summary)
    with res_col2:
        st.subheader("📝 Comment")
        st.code(st.session_state.comment, language=None)
    
    if st.button("🔄 Reset"):
        del st.session_state.summary
        del st.session_state.comment
        st.rerun()
