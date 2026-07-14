import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

st.markdown("""
    <style>
    :root { --talabat-orange: #FF7800; }
    .stButton>button { background-color: var(--talabat-orange) !important; color: white !important; border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic (Definitions for the AI to understand the 'Stance')
DRIVE_MAP = {
    "Follow up on existing case": "Customer is checking on a raised case (Complaints/Refund/tRewards/Escalation).",
    "Contactless delivery feature inquiry": "Customer is asking about the contactless rules and procedures.",
    "Payment method inquiry": "Inquiry on changing payment methods, adding/removing cards, or refund reversals.",
    "Partner related inquiry": "Inquiries about vendor availability, menu, hours, Halal confirmation, etc.",
    "Rider related inquiry": "Inquiries on tipping, rating, or contacting the rider.",
    "Delivery area/fee inquiry": "Inquiries about delivery coverage, high fees, or COD/Express fee disputes.",
    "Promotions/deals/Gift Card": "Subscription, newsletter, or E-Gift card inquiries.",
    "Non-live order inquiry": "General queries (pre-order, utensils, general ordering process).",
    "Loyalty program inquiry": "Inquiry regarding subscription or loyalty programs.",
    "Work with us": "Partnership or employment inquiries.",
    "Logistics as a service inquiry": "Partner logistics service requests.",
    "Positive": "Positive feedback or review resolution.",
    "Negative": "Negative feedback or compensation dissatisfaction.",
    "Spam / Irrelevant": "Silent chats or irrelevant inquiries.",
    "Menu price discrepancy": "Price markup complaints (Pre-order stage).",
    "Mistake on menu": "Errors on frontend/application (Pre-order stage)."
}

# 3. State
if "summary" not in st.session_state: st.session_state.summary = ""
if "comment" not in st.session_state: st.session_state.comment = ""

# 4. Header
st.title("🍔 Talabat Log Tool")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. UI Input
chat_input = st.text_area("Paste Transcript:", height=150)
selected_drive = st.selectbox("Select Contact Drive (Context):", options=list(DRIVE_MAP.keys()))

if st.button("🚀 Generate Professional Log"):
    if chat_input:
        with st.spinner('Analyzing...'):
            context_desc = DRIVE_MAP[selected_drive]
            
            prompt = f"""
            You are a Senior Talabat Agent. Analyze the transcript based on the following Context:
            CONTACT DRIVE: {selected_drive}
            CONTEXT/DEFINITION: {context_desc}
            
            Instructions:
            - Write a professional, human-readable SUMMARY of the interaction.
            - Write a detailed, technical COMMENT (Log) focusing on the Resolution and Action Taken.
            - DO NOT use templates or rigid syntax. Write natural, high-quality English.
            - Focus on: What was the issue? What did we do? What is the outcome?
            
            Output format (Strictly use these tags):
            [SUMMARY]
            ...
            [COMMENT]
            ...
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.5
                )
                raw_text = response.choices[0].message.content
                
                # Parsing the result
                sum_match = re.search(r'\[SUMMARY\](.*?)\[COMMENT\]', raw_text, re.DOTALL)
                com_match = re.search(r'\[COMMENT\](.*)', raw_text, re.DOTALL)
                
                st.session_state.summary = sum_match.group(1).strip() if sum_match else "Could not parse summary."
                st.session_state.comment = com_match.group(1).strip() if com_match else raw_text
                
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Display Result in Tabs
if st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Resolution Log (Comment)"])
    
    with tab1:
        st.write(st.session_state.summary)
        
    with tab2:
        st.write(st.session_state.comment)
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.comment = ""
        st.rerun()
