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
    "Order tracking issue TMP & TGO", "Order will not be processed (Cancellation)",
    "Need help locating partner for pickup", "Complaint about short delay", "Complaint about moderate delay",
    "Complaint about severe delay", "Complaint about extreme delay", "Missing item", "Wrong item", 
    "Wrong order", "Order never arrived", "Spilled food", "Food quality", "Food temperature",
    "Food poisoning", "Missing equipment/uniform", "Order not delivered to doorstep", "Refund query",
    "Refund request", "Double Charge", "Damaged item", "Voucher request", "Voucher not received",
    "Follow up on existing case", "Positive", "Negative", "Spam / Irrelevant"
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
selected_drive = st.selectbox("Select Contact Drive:", options=CONTACT_DRIVES) # الـ Scroll رجعت هنا!

if st.button("🚀 Generate Distinct Variations"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Generating professional, distinct variants...'):
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            CONTACT DRIVE: {selected_drive}
            
            CORE INSTRUCTION:
            - Variation A: Focus on Empathy and Apology.
            - Variation B: Focus on Resolution and Action Taken.
            - Variation C: Focus on Policy and Process explanation.
            - Variation D: Focus on Conciseness and Speed.
            
            Generate the [COMMENT] section strictly in this dense format:
            [Issue Category] // [Status/Logic Details] (( [Sub-logic details] )) // [Outcome] // [Next Steps] // [Info Channel]
            
            Format tags: [OPTION_A], [OPTION_B], [OPTION_C], [OPTION_D].
            Inside each:
            [SUMMARY]: ...
            [COMMENT]: ...
            
            RULES: 
            - NO Order ID.
            - NO Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.7
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
        st.markdown("### Choose the Best Option:")
        for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
            with st.container(border=True):
                st.subheader(f"Option {opt_label}")
                st.code(options[i], language=None)
                if st.button(f"✅ Vote & Train {opt_label}", key=f"btn_{opt_label}"):
                    st.session_state.selected_result = options[i]
                    st.session_state.golden_examples.append(options[i])
                    st.session_state.voted = True
                    st.rerun()
    else:
        st.warning("AI output format error. Showing raw output:")
        st.code(raw)

if st.session_state.voted:
    st.divider()
    st.success("🎉 Learned! Select 'Reset' to clear.")
    if st.button("🔄 Reset"):
        st.session_state.voted = False
        st.session_state.raw_response = None
        st.rerun()
