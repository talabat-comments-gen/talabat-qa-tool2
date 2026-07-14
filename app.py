import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat comment tool", layout="wide")

# 2. Updated Master List (Categorized and Cleaned)
DRIVE_LIST = [
    # Delays
    "Delay: Short (0-10 min)", "Delay: Moderate (11-20 min)", "Delay: Severe (21-30 min)", "Delay: Extreme (+30 min)",
    "Delay: ETA stuck/increasing (TGO)", "Delay: Order marked delivered but not received (TGO)",
    
    # Cancellations & Requests
    "Cancellation: Partner/Logistics/Shield", "Cancellation: Accidental/Duplicated", "Cancellation: Change of mind",
    "Request: Order modification (Address/Items/Time)", "Request: Voucher not applied",
    
    # Order Issues
    "Issue: Missing item / Wrong item", "Issue: Spilled food / Packaging", "Issue: Food quality / Temp / Allergens",
    "Issue: Foreign Object", "Issue: Cooking instructions not followed", "Issue: Food portion / Extra item",
    "Issue: Wrong order / Never arrived", "Issue: Inappropriate behavior (Rider)",
    "Issue: Money collection / Change issues", "Issue: Invoice missing / Incorrect details",
    
    # Payments & Vouchers
    "Refund Query", "Double Charge", "Wallet / Credit issues", "Voucher Inquiry (Validity/Conditions/Cannot apply)",
    "Payment Method Inquiry (Change/Method clarification)",
    
    # Account & Tech
    "Website / App Issue", "Account Deletion / Data Protection", "Subscription / Premium (T-Pro)",
    "Loyalty Program / Rewards", "SMS Verification issue",
    
    # General Inquiries
    "Check order status / Confirmation missing", "Partner Inquiry (Availability/Menu/Halal)", 
    "Rider Inquiry (Contact/Rating/Tip)", "Delivery Area / Fee Inquiry", 
    "Pick-up specific issues (Locating/Outlet/Time)", "Non-live order inquiry (General)",
    
    # Feedback & Other
    "Positive Feedback", "Negative Feedback", "Spam / Irrelevant", "Menu Price Discrepancy", "Mistake on menu"
]

# 3. UI
st.title("🍔 talabat comment tool")
st.markdown("---")

col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    chat_input = st.text_area("Paste Chat Transcript:", height=150)
with col_input2:
    selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_LIST)

if st.button("🚀 Generate"):
    if chat_input:
        with st.spinner('Analyzing...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are a strict Talabat Log Generator. Analyze the transcript for: {selected_drive}.
            
            OUTPUT FORMAT (MUST FOLLOW THIS EXACTLY):
            SUMMARY: [One single sentence summary of the issue]
            COMMENT: [Issue/Context] // [Action 1] // [Action 2] // [Resolution/Comp] // [Outcome]
            
            RULES:
            1. No greetings, no endings, no "Happy to help", no "Dear customer", no survey mentions.
            2. Strict format for COMMENT: [Issue] // [Action] // [Action] // [Res] // [Outcome].
            3. Use technical abbreviations (CST, RST, OT, comp, cst info).
            4. No Arabic in the output (English only).
            5. Be factual, technical, and concise.
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

# 4. Result Display
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
