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

# 2. Detailed Contact Drives Logic
DRIVE_MAP = {
    "Follow up on existing case": "Customer is checking on a raised case (Complaints/Refund/tRewards/tPro/Escalation). Handle incomplete orders, double deduction, or payment issues. Address if promised compensation was not applied.",
    "Contactless delivery feature inquiry": "Customer is asking about the contactless rules and procedures that Talabat follows.",
    "Payment method inquiry": "Inquiry on changing/deleting payment methods, adding/removing credit cards, or how to pay via specific methods. Also covers requests to revert refunds to bank.",
    "Partner related inquiry": "Inquiries about vendor availability, menu selection, operational hours, Halal confirmation, or how to contact the restaurant.",
    "Rider related inquiry": "Inquiries on tipping, rating the rider, or contacting the rider.",
    "Delivery area/fee inquiry": "Inquiries about delivery coverage, high delivery fees, or issues regarding Cash on Delivery (COD) / Express Delivery fees.",
    "Promotions and deals inquiry": "Details on subscription programs, newsletter signup, or E-Gift cards.",
    "Non-live order inquiry": "General inquiries not related to a live order (e.g., pre-ordering, utensils, general ordering process).",
    "Loyalty program inquiry": "Inquiry regarding subscription or loyalty programs.",
    "Work with us": "Inquiries regarding employment or partnership with Talabat.",
    "Logistics as a service inquiry": "Inquiries from partners who want to use Talabat's logistics services.",
    "Positive": "Positive feedback for Talabat or the restaurant. Handle rating/review issues (Positive).",
    "Negative": "Negative feedback or dissatisfaction with compensation amount. Handle rating/review issues (Negative).",
    "Spam / Irrelevant": "Silent chats or general inquiries unrelated to Talabat.",
    "Menu price discrepancy": "Complaint about price markup issue (Pre-order).",
    "Mistake on menu": "Errors on frontend/application (Pre-order)."
}

# 3. State Management
if "generated_comment" not in st.session_state: st.session_state.generated_comment = None

# 4. Header
st.title("🍔 Talabat Log Generator")
st.markdown("### Professional Resolution & Action Logging")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Input Section
chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
selected_drive = st.selectbox("Select Contact Drive (Context dictates stance):", options=list(DRIVE_MAP.keys()))

if st.button("🚀 Generate Final Resolution Log"):
    if chat_input:
        with st.spinner('Analyzing stance and crafting log...'):
            
            # بنبعت للـ AI الاسم + التعريف بتاعه
            selected_desc = DRIVE_MAP[selected_drive]
            
            prompt = f"""
            You are a Senior Talabat Agent. Your goal is to write ONE comprehensive, professional, and detailed log comment based on the chat transcript.
            
            CONTACT DRIVE: {selected_drive}
            CONTEXT/DEFINITION: {selected_desc}
            
            CORE INSTRUCTION:
            - Analyze the transcript through the lens of the provided definition.
            - Focus HEAVILY on Resolution and Action Taken.
            - The comment must be technical, dense, and professional.
            
            Format strictly in this dense format:
            [Issue Category] // [Status/Logic Details] (( [Sub-logic details: Resolution and Actions taken] )) // [Outcome] // [Next Steps] // [Info Channel]
            
            RULES: 
            - NO Order ID.
            - NO Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            - The output must be ONE long, dense paragraph of technical details.
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
