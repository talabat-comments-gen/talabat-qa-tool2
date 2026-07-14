import streamlit as st
import os
from groq import Groq

# 1. Config & Styling
st.set_page_config(page_title="Talabat Log Generator", layout="centered", page_icon="🍔")

st.markdown("""
    <style>
    :root { --talabat-orange: #FF7800; }
    .stButton>button {
        background-color: var(--talabat-orange) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover { background-color: #e66c00 !important; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 2. Comprehensive Drive Map (Full List)
DRIVE_MAP = {
    "Check order status": "Checking current order progress, location, or ETA.",
    "Complain about late order - tMP & tGO": "Delayed order in TMP or TGO delivery. Needs investigation.",
    "ETA is stuck or increasing (TGO)": "TGO delivery ETA is not updating or increasing.",
    "Order marked as delivered but didn't receive (TGO)": "System shows delivered but customer claims non-receipt.",
    "Restaurant hasn't started preparing the food (TGO)": "Restaurant latency issues.",
    "Didn't receive order confirmation": "Technical issue or delay in receiving order confirmation.",
    "Order tracking issue TMP & TGO": "Issue with real-time tracking visibility.",
    "Order will not be processed (Cancellation)": "Order cancelled due to various reasons.",
    "Cancellation reason inquiry": "Customer asking why an order was cancelled.",
    "Order not assigned to rider": "Logistics issue, rider not found/assigned.",
    "Need help locating partner for pickup": "Pickup issue, location/contact clarification.",
    "Item unavailable for pickup": "Partner issue, item stock out.",
    "Complaint about short/moderate/severe/extreme delay": "Addressing specific delay durations and corresponding compensation/action.",
    "Address/Delivery issues": "Address correction, delivery instructions not followed.",
    "Food items/Cooking instructions": "Issues with food preparation or ingredients.",
    "Payment method/Voucher/Contact Details": "Inquiries on payments, voucher applications, or profile updates.",
    "Change expedition type/time/outlet": "Request to modify pickup or delivery parameters.",
    "Missing/Wrong item/Order/Spilled food": "Quality or accuracy complaints (Missing, Wrong, Spilled).",
    "Food quality/Temperature/Poisoning/Allergens": "Food safety and quality issues.",
    "Foreign Object": "Safety escalation (Foreign object in food).",
    "Inappropriate behavior": "Conduct complaint against rider/partner.",
    "Money collection/Delivery instructions": "Cash collection or instruction follow-through.",
    "Invoice issues": "Missing or incorrect invoice details.",
    "Refunds/Wallet/Double Charge": "Financial escalations, double charges, or refund requests.",
    "Website/App/Online payment issues": "Technical platform issues.",
    "Account/Subscription/Loyalty/Premium/Rewards": "Account management and program inquiries.",
    "Follow up on existing case": "Status check on raised complaints/refunds/escalations.",
    "Contactless delivery feature inquiry": "Rules/procedures for contactless delivery.",
    "Partner related inquiry": "Vendor availability, menu, hours, halal status, or contact requests.",
    "Rider related inquiry": "Tipping, rating, or contacting rider.",
    "Delivery area/fee inquiry": "Delivery area coverage or fee/COD/Express fee disputes.",
    "Promotions/deals/Gift Card": "Subscription, newsletter, or E-Gift card inquiries.",
    "Non-live order inquiry": "General queries (pre-order, utensils, etc.) without an active order.",
    "Work with us": "Partnership or employment inquiries.",
    "Logistics as a service inquiry": "Partner logistics service requests.",
    "Positive": "Positive feedback or review resolution.",
    "Negative": "Negative feedback or compensation dissatisfaction.",
    "Spam / Irrelevant": "Silent or non-relevant chats.",
    "Menu price discrepancy": "Price markup complaints (Pre-order).",
    "Mistake on menu": "Frontend/Application menu errors."
}

# 3. State Management
if "generated_comment" not in st.session_state: st.session_state.generated_comment = None

# 4. Header
st.title("🍔 Talabat Log Generator")
st.markdown("### Full Resolution & Action Log")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Input Section
chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
selected_drive = st.selectbox("Select Contact Drive (Context dictates stance):", options=list(DRIVE_MAP.keys()))

if st.button("🚀 Generate Final Resolution Log"):
    if chat_input:
        with st.spinner('Analyzing stance and crafting log...'):
            selected_desc = DRIVE_MAP[selected_drive]
            
            prompt = f"""
            You are a Senior Talabat Agent. Write ONE comprehensive, professional, technical log comment.
            
            CONTACT DRIVE: {selected_drive}
            CONTEXT: {selected_desc}
            
            CORE INSTRUCTION:
            - Analyze the transcript using the provided Context.
            - Focus HEAVILY on Resolution and Action Taken.
            - Ensure the tone is technical, objective, and dense.
            
            Format strictly in this dense format:
            [Issue Category] // [Status/Logic Details] (( [Sub-logic details: Resolution and Actions taken] )) // [Outcome] // [Next Steps] // [Info Channel]
            
            RULES: 
            - NO Order ID.
            - NO Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            - The output must be ONE long, dense paragraph.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.5
                )
                st.session_state.generated_comment = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 6. Display Result
if st.session_state.generated_comment:
    st.markdown("### ✅ Final Resolution Log")
    with st.container(border=True):
        st.write(st.session_state.generated_comment)
        
    if st.button("🔄 Reset"):
        st.session_state.generated_comment = None
        st.rerun()
