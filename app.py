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
    "Complaint about short delay (0-10 mins)": "Delivery time exceeded by 0-10 mins.",
    "Complaint about moderate delay (11-20 mins)": "Delivery time exceeded by 11-20 mins.",
    "Complaint about severe delay (21-30 mins)": "Delivery time exceeded by 21-30 mins.",
    "Complaint about extreme delay (+30 mins)": "Delivery time exceeded by +30 mins.",
    "Check order status": "Checking current order progress, location, or ETA.",
    "Follow up on existing case": "Status check on raised complaints/refunds/escalations.",
    "Refunds/Wallet/Double Charge": "Financial escalations, double charges, or refund requests.",
    "Partner related inquiry": "Vendor availability, menu, hours, halal status, or contact requests.",
    "Positive": "Positive feedback or review resolution.",
    "Negative": "Negative feedback or compensation dissatisfaction."
    # (يمكنك إضافة باقي الـ Drives هنا بنفس الطريقة)
}

# 3. State Management
if "generated_comment" not in st.session_state: st.session_state.generated_comment = None

# 4. Header
st.title("🍔 Talabat Log Generator")
st.markdown("### Strict Format: Resolution & Action")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Input Section
chat_input = st.text_area("Paste Chat Transcript:", height=150, placeholder="Paste conversation here...")
selected_drive = st.selectbox("Select Contact Drive:", options=list(DRIVE_MAP.keys()))

if st.button("🚀 Generate Log"):
    if chat_input:
        with st.spinner('Formatting log...'):
            selected_desc = DRIVE_MAP[selected_drive]
            
            # التعديل الجوهري في الـ Prompt عشان يلتزم بالفورمات الصارم
            prompt = f"""
            You are a Senior Talabat Agent. Write a professional log based on the transcript.
            
            CONTACT DRIVE: {selected_drive}
            CONTEXT: {selected_desc}
            
            CORE INSTRUCTION:
            1. SUMMARY: Write a short, human-readable summary of the case.
            2. COMMENT: Write the log EXTREMELY strictly in this pattern:
            [Contact Drive] // asper last comment ((OT // status // asper last comment //////// “cst message”, “+++comment actual action”, //////// next steps )) // Outcome // Next Steps // Info Channel
            
            RULES:
            - Use the exact double quotes, slashes, and nested parentheses provided in the pattern.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            - No Arabic.
            - No Order ID.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.3
                )
                st.session_state.generated_comment = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 6. Display Result
if st.session_state.generated_comment:
    st.markdown("### ✅ Final Output")
    with st.container(border=True):
        st.write(st.session_state.generated_comment)
        
    if st.button("🔄 Reset"):
        st.session_state.generated_comment = None
        st.rerun()
