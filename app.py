import streamlit as st
import os
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
    "Order tracking issue TMP & TGO", "Order will not be processed (Cancellation)",
    "Need help locating partner for pickup", "Complaint about short delay", "Complaint about moderate delay",
    "Complaint about severe delay", "Complaint about extreme delay", "Missing item", "Wrong item", 
    "Wrong order", "Order never arrived", "Spilled food", "Food quality", "Food temperature",
    "Food poisoning", "Missing equipment/uniform", "Order not delivered to doorstep", "Refund query",
    "Refund request", "Double Charge", "Damaged item", "Voucher request", "Voucher not received",
    "Follow up on existing case", "Positive", "Negative", "Spam / Irrelevant"
]

# 3. State Management
if "generated_comment" not in st.session_state: st.session_state.generated_comment = None

# 4. Header
st.title("🍔 Talabat Comment Generator")
st.markdown("### Focus: Resolution & Action Taken")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Input Section
chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
selected_drive = st.selectbox("Select Contact Drive (Sets the Case Stance):", options=CONTACT_DRIVES)

if st.button("🚀 Generate Final Comment"):
    if chat_input:
        with st.spinner('Crafting the perfect resolution log...'):
            
            prompt = f"""
            You are a Senior Talabat Agent. Your goal is to write ONE comprehensive, professional, and detailed log comment based on the chat transcript and the selected Contact Drive.
            
            CONTACT DRIVE: {selected_drive}
            
            CORE INSTRUCTION:
            - Focus HEAVILY on Resolution and Action Taken.
            - Explain the stance of the case clearly based on the Contact Drive provided.
            - Ensure the tone is professional, technical, and objective.
            
            Format strictly in this dense format:
            [Issue Category] // [Status/Logic Details] (( [Sub-logic details: Resolution and Actions taken] )) // [Outcome] // [Next Steps] // [Info Channel]
            
            RULES: 
            - NO Order ID.
            - NO Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            - The output must be ONE long paragraph of dense technical details.
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
