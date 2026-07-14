import streamlit as st
import os
import time
from groq import Groq

# 1. Page Config & Professional Branding
st.set_page_config(page_title="Talabat Surgical Pro v3", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .animated-result { animation: fadeIn 0.6s ease-out; }
    </style>
""", unsafe_allow_html=True)

# 2. Dictionary of Abbreviations
abbreviations = {
    "CST / Cust": "Customer", "RST / Rest": "Restaurant", "WDT": "Within Delivery Time",
    "RNA": "Restaurant/Rider Not Answering", "FU": "Follow Up", "OTW": "On The Way",
    "ROP": "Restaurant Operator", "SLA": "Service Level Agreement", "ASAP": "As Soon As Possible",
    "Info": "Informed", "TC": "Talabat Credit", "ETA": "Estimated Time Arrival",
    "R&V": "Refund & Validation", "OT": "Offline Ticket", "T&C": "Terms & Condition",
    "SPV": "Supervisor", "TL": "Team Leader", "SME": "Subject Matter Expert",
    "VP": "Vendor Portal", "PDT / DT": "Promise Delivery Time / Delivery Time",
    "PIC": "Picture", "SS": "Screenshot", "Ven": "Vendor", "Comp": "Compensation",
    "WFA": "Waiting For Answer", "OSU": "Referring to R&V", "EDT": "Exceeded Delivery Time",
    "NFA": "No further action required", "NAT": "No action taken", "NFAT": "No further action taken",
    "Bot": "Chatbot", "SOP": "Standard Operation Procedures", "HVC": "High-Value Customer",
    "App": "Application", "CNA / NA": "Customer Not Answering", "BOA": "Backoffice",
    "Min / Mins": "Minute(s)", "CBH": "Customer Bad History", "CGH": "Customer Good History",
    "Msg": "Message", "Under Prep": "Under Preparation", "Dr": "Doctor",
    "H / hrs": "Hour(s)", "HC": "Hero Care", "BRB": "Be Right Back",
    "PR": "Partial Refund", "FR": "Full Refund", "T2": "Tier 2", "T3": "Tier 3",
    "ANS": "Answered", "Num": "Number", "SMS": "Short Message Service",
    "Acc": "Account", "RM": "Rider Manager", "AM": "Account Manager",
    "MCB": "Manager Call Back", "BL": "Backlog"
}

st.title("🚀 Talabat Surgical Pro v3")

# Glossary Expander
with st.expander("📚 Abbreviations Glossary"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Extract Data (Maximum Precision)"):
    if chat_input:
        # 3. Countdown Animation
        with st.spinner('Initializing Surgical Systems...'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i in range(5):
                time.sleep(1) # 5 seconds delay
                progress_bar.progress((i + 1) * 20)
                status_text.text(f"Analyzing nuance {i+1}/5...")
            status_text.text("Analysis Complete!")

        # 4. Processing
        try:
            system_prompt = """
            You are a Surgical Data Extraction Engine. 
            PRECISION LEVEL: 200%. 
            
            YOUR MISSION:
            1. Read the chat.
            2. Sharp Summary: Write one single, punchy, professional sentence summarizing the issue in English.
            3. Extract Data: Identify 4 distinct, non-repetitive, highly accurate data points.
            
            STRICT RULES:
            - Output format:
              [SUMMARY]: (One professional English sentence)
              [DATA]:
              [Issue] // [Details] // [Action] // [Order ID]
            
            - SYSTEM LOGIC: If agent is restricted, ALWAYS write: 'no action taken'.
            - TRANSLATION: Literal translation from Arabic to English. NO ARABIC in output.
            - Order ID: Numeric only. If invalid, 'N/A'.
            - NO filler, NO headers, JUST the Summary and Data.
            """

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Transcript: {chat_input}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.0
            )
            
            raw_output = chat_completion.choices[0].message.content
            
            # Parsing
            summary = ""
            data_points = []
            if "[SUMMARY]:" in raw_output and "[DATA]:" in raw_output:
                summary = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")[0].strip()
                data_raw = raw_output.split("[DATA]:")[1].strip()
                data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]

            # Display
            st.metric("Points Extracted", len(data_points))
            st.subheader("Sharp Summary")
            st.info(summary)
            
            st.subheader("Surgical Breakdown")
            st.markdown('<div class="animated-result">', unsafe_allow_html=True)
            for point in data_points:
                st.code(point, language=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please paste the chat transcript.")
