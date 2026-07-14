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

# 2. Comprehensive Drive Map
DRIVE_MAP = {
    "Check order status": "Checking current order progress, location, or ETA.",
    "Complain about short delay (0-10 mins)": "Delivery time exceeded by 0-10 mins.",
    "Complaint about moderate delay (11-20 mins)": "Delivery time exceeded by 11-20 mins.",
    "Complaint about severe delay (21-30 mins)": "Delivery time exceeded by 21-30 mins.",
    "Complaint about extreme delay (+30 mins)": "Delivery time exceeded by +30 mins.",
    "Order marked as delivered but didn't receive (TGO)": "System shows delivered but customer claims non-receipt.",
    "Restaurant hasn't started preparing the food (TGO)": "Restaurant latency issues.",
    "Didn't receive order confirmation": "Technical issue or delay in receiving order confirmation.",
    "Order tracking issue TMP & TGO": "Issue with real-time tracking visibility.",
    "Order will not be processed (Cancellation)": "Order cancelled due to various reasons.",
    "Cancellation reason inquiry": "Customer asking why an order was cancelled.",
    "Order not assigned to rider": "Logistics issue, rider not found/assigned.",
    "Need help locating partner for pickup": "Pickup issue, location/contact clarification.",
    "Item unavailable for pickup": "Partner issue, item stock out.",
    "Address / Delivery instructions": "Address correction or delivery instructions not followed.",
    "Food items / Cooking instructions": "Issues with food preparation or ingredients.",
    "Payment method / Voucher / Contact Details": "Inquiries on payments, voucher applications, or profile updates.",
    "Change expedition type / pick-up time / outlet": "Request to modify pickup or delivery parameters.",
    "Request: order is late / longer than expected": "Request for delay updates.",
    "Request: changed mind / accidental / duplicated": "Order cancellation/modification requests.",
    "Complaint: Partner/logistics cancellation": "Partner closed or cancelled due to issues.",
    "Missing item / Wrong item / Wrong order / Spilled food": "Quality or accuracy complaints.",
    "Food quality / Temperature / Poisoning / Allergens": "Food safety and quality issues.",
    "Foreign Object": "Safety escalation (Foreign object in food).",
    "Inappropriate behavior": "Conduct complaint against rider/partner.",
    "Money collection issue": "Cash collection or instruction follow-through.",
    "Invoice missing / Incorrect details": "Missing or incorrect invoice details.",
    "Refund query / Wallet refund / Double Charge": "Financial escalations, double charges, or refund requests.",
    "Website / App / Online / Offline payment issues": "Technical platform issues.",
    "Account deletion / Data protection": "Account management and data privacy inquiries.",
    "Subscription / Premium / Loyalty program": "Account management and program inquiries.",
    "Follow up on existing case": "Status check on raised complaints/refunds/escalations.",
    "Contactless delivery feature inquiry": "Rules/procedures for contactless delivery.",
    "Payment method inquiry": "Changing payment methods or refund reversals.",
    "Partner related inquiry": "Vendor availability, menu, hours, halal status, or contact requests.",
    "Rider related inquiry": "Tipping, rating, or contacting rider.",
    "Delivery area/fee inquiry": "Delivery area coverage or fee/COD/Express fee disputes.",
    "Promotions / deals / E-Gift Card": "Subscription, newsletter, or E-Gift card inquiries.",
    "Non-live order inquiry": "General queries (pre-order, utensils, etc.) without an active order.",
    "Work with us": "Partnership or employment inquiries.",
    "Logistics as a service inquiry": "Partner logistics service requests.",
    "Positive": "Positive feedback or review resolution.",
    "Negative": "Negative feedback or compensation dissatisfaction.",
    "Spam / Irrelevant": "Silent chats or irrelevant inquiries.",
    "Menu price discrepancy": "Price markup complaints (Pre-order).",
    "Mistake on menu": "Frontend/Application menu errors."
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
        with st.spinner('Analyzing stance and crafting log...'):
            context_desc = DRIVE_MAP[selected_drive]
            
            prompt = f"""
            You are a Senior Talabat Agent. Analyze the transcript based on:
            CONTACT DRIVE: {selected_drive}
            CONTEXT: {context_desc}
            
            Instructions:
            - Write a professional, human-readable SUMMARY of the interaction.
            - Write a detailed, technical COMMENT (Log) focusing on the Resolution and Action Taken.
            - DO NOT use templates or rigid syntax. Write natural, high-quality professional English.
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
                
                # Parsing
                sum_match = re.search(r'\[SUMMARY\](.*?)\[COMMENT\]', raw_text, re.DOTALL)
                com_match = re.search(r'\[COMMENT\](.*)', raw_text, re.DOTALL)
                
                st.session_state.summary = sum_match.group(1).strip() if sum_match else "Could not parse summary."
                st.session_state.comment = com_match.group(1).strip() if com_match else raw_text
                
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Display Result
if st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Resolution Log (Comment)"])
    with tab1: st.write(st.session_state.summary)
    with tab2: st.write(st.session_state.comment)
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.comment = ""
        st.rerun()
