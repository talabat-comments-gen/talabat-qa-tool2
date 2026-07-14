import streamlit as st
import os
import re
from groq import Groq

# 1. Config & Styling
st.set_page_config(page_title="Talabat Comment Generator", layout="centered", page_icon="🍔")

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

# 2. Options List
CONTACT_DRIVES = [
    "Check order status", "Complain about late order - tMP & tGO", "ETA is stuck or increasing (TGO)",
    "Order marked as delivered but didn't receive (TGO)", "Restaurant hasn't started preparing the food (TGO)",
    "Didn't receive order confirmation", "Order tracking issue TMP & TGO", "Order will not be processed (Cancellation)",
    "Cancellation reason inquiry", "Order not assigned to rider", "Need help locating partner for pickup",
    "Item unavailable for pickup", "Complaint about short delay", "Complaint about moderate delay",
    "Complaint about severe delay", "Complaint about extreme delay", "Address", "Food items", "Delivery instructions",
    "Delivery time/date", "Cooking instructions", "Payment method", "Voucher", "Contact Details",
    "Change expedition type", "Change pick-up time", "Change pick-up outlet", "Request: order will take longer than expected",
    "Request: voucher not applied", "Request: order modification not possible", "Request: order is late",
    "Request: changed mind", "Request: accidental order", "Request: duplicated order",
    "Complaint: Partner cancellation", "Complaint: logistics cancellation", "Request: Partner closed for pickup",
    "Request: Unable to locate pickup partner", "Request: out of stock item(s)", "Missing item",
    "Wrong item", "Issue with item replacement process", "Wrong order", "Order never arrived", "Spilled food",
    "Food quality", "Cooking instructions were not followed", "Food portion", "Food temperature",
    "Food poisoning", "Food allergens - complain", "Foreign Object", "Short delay - TGO", "Inappropriate behavior",
    "Missing equipment/uniform", "Order not delivered to doorstep", "Money collection issue",
    "Delivery instructions not followed", "Invoice missing", "Incorrect invoice", "Incorrect invoice details",
    "Refund query", "Refund request", "Wallet refund query", "Double Charge", "Rider Tips refund issue",
    "Expired item", "Damaged item", "Near expiry date", "Product Quantity", "Other issues related to Contactless delivery",
    "Website issue", "App issue", "Online payment issue", "Offline payment issue", "Wallet issue",
    "Voucher validity", "Voucher conditions", "Voucher already used", "Cannot apply", "Not satisfied with value",
    "Voucher request", "Voucher not received", "Other voucher inquiry", "Promotion/discount not applied",
    "Newsletter un-subscription", "Account deletion", "Data protection inquiry", "Change account details",
    "SMS Verification issue", "Subscription / Premium service issue", "Loyalty program issue",
    "Dine-in deals issue", "Reward program issue", "Follow up on existing case", "Contactless delivery feature inquiry",
    "Payment method inquiry", "Partner related inquiry", "Rider related inquiry", "Delivery area/fee inquiry",
    "Promotions and deals inquiry", "Non-live order inquiry", "Loyalty program inquiry", "Work with us",
    "Logistics as a service inquiry", "Positive", "Negative", "Spam / Irrelevant",
    "Menu price discrepancy", "Mistake on menu"
]

# 3. State Management
if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "voted" not in st.session_state: st.session_state.voted = False
if "raw_response" not in st.session_state: st.session_state.raw_response = None
if "selected_result" not in st.session_state: st.session_state.selected_result = ""

# 4. Header
st.title("🍔 Talabat Comment Generator")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Input Section
chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
selected_drive = st.selectbox("Select Contact Drive:", options=CONTACT_DRIVES, index=0)

if st.button("Generate Variations"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Generating professional logs...'):
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            CONTACT DRIVE: {selected_drive}
            
            CORE INSTRUCTION: 
            Generate the [COMMENT] section strictly in this dense format:
            [Issue Category] // [Status/Logic Details] (( [Sub-logic details] )) // [Outcome] // [Next Steps] // [Info Channel]
            
            Format tags: [OPTION_A], [OPTION_B], [OPTION_C], [OPTION_D].
            Inside each:
            [SUMMARY]: ...
            [COMMENT]: ... (Follow the strict format above)
            
            RULES: 
            - NO Order ID.
            - NO Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            - Ensure the COMMENT section looks exactly like a technical log.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.0
                )
                st.session_state.raw_response = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 6. Parsing & Display
if st.session_state.raw_response:
    raw = st.session_state.raw_response
    parts = re.split(r'\[OPTION_[A-D]\]', raw)
    options = [p.strip() for p in parts if p.strip()]

    if len(options) >= 4:
        if not st.session_state.voted:
            st.markdown("### Choose the Best Option:")
            for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
                with st.container(border=True):
                    st.subheader(f"Option {opt_label}")
                    st.code(options[i], language=None)
                    if st.button(f"Vote {opt_label}", key=f"btn_{opt_label}"):
                        st.session_state.selected_result = options[i]
                        st.session_state.golden_examples.append(options[i])
                        st.session_state.voted = True
                        st.rerun()
        else:
            st.success("✅ Log saved.")
            if st.button("🔄 Reset"):
                st.session_state.voted = False
                st.rerun()
    else:
        st.code(raw)

if st.session_state.voted:
    st.divider()
    st.subheader("Selected Final Report")
    with st.container(border=True):
        st.code(st.session_state.selected_result, language=None)
