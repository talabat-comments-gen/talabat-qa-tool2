import streamlit as st
import os
import time
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Surgical Pro v5", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v5 (Intent Engine)")

# 2. Abbreviations
abbreviations = {
    "CST/Cust": "Customer", "RST/Rest": "Restaurant", "WDT": "Within Delivery Time",
    "RNA": "Restaurant/Rider Not Answering", "FU": "Follow Up", "OTW": "On The Way",
    "ROP": "Restaurant Operator", "SLA": "Service Level Agreement", "ASAP": "As Soon As Possible",
    "Info": "Informed", "TC": "Talabat Credit", "ETA": "Estimated Time Arrival",
    "R&V": "Refund & Validation", "OT": "Offline Ticket", "T&C": "Terms & Condition",
    "SPV": "Supervisor", "TL": "Team Leader", "SME": "Subject Matter Expert",
    "VP": "Vendor Portal", "PDT/DT": "Promise Delivery Time", "PIC": "Picture",
    "SS": "Screenshot", "Ven": "Vendor", "Comp": "Compensation", "WFA": "Waiting For Answer",
    "OSU": "Referring to R&V", "EDT": "Exceeded Delivery Time", "NFA": "No further action",
    "NAT": "No action taken", "NFAT": "No further action taken", "Bot": "Chatbot",
    "SOP": "Standard Operation Procedures", "HVC": "High-Value Customer",
    "CBH": "Customer Bad History", "CGH": "Customer Good History", "PR": "Partial Refund",
    "FR": "Full Refund", "BL": "Backlog", "MCB": "Manager Call Back"
}

with st.expander("📚 Abbreviations Glossary"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Analyze Intent & Extract"):
    if chat_input:
        with st.spinner('Analyzing Intent...'):
            try:
                system_prompt = """
                You are a Senior Linguistic Analyst.
                YOUR MISSION: Analyze the chat deeply. Determine the *Intent* of the customer for every segment.
                
                STEP 1: CLASSIFY INTENT
                Assign one of these types:
                - Complaint: Something is wrong/failed.
                - Clarification: Providing context or correcting info.
                - Request: Asking for action/help.
                - Status Check: Checking order status.
                
                STEP 2: EXTRACTION
                Format: [Type] // [Issue/Context] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - NO ARABIC in output.
                - Literal translation (Syntactically accurate).
                - 'no action taken' for system restrictions.
                - 'N/A' for invalid IDs.
                - Final Output: Professional, ready-to-copy report.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                # Output logic
                raw_output = chat_completion.choices[0].message.content
                lines = [line.strip() for line in raw_output.split('\n') if line.strip()]
                
                st.subheader("Analysis Breakdown")
                for line in lines:
                    st.code(line, language=None)
            
            except Exception as e:
                st.error(f"Error: {e}")
