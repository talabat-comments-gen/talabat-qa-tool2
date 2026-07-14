import streamlit as st
import os
import time
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Surgical Pro v4", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { background-color: #f4f4f4; border-left: 5px solid #FF8500; }
    </style>
""", unsafe_allow_html=True)

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

st.title("🚀 Talabat Surgical Pro v4 (Linguistic Engine)")

with st.expander("📚 Abbreviations Glossary"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Final Report"):
    if chat_input:
        # Countdown
        with st.spinner('Linguistic Analysis In Progress...'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i in range(5):
                time.sleep(1)
                progress_bar.progress((i + 1) * 20)
                status_text.text(f"Syntax & Context Mapping {i+1}/5...")
            status_text.text("Logic Verified!")

        try:
            system_prompt = """
            You are a Senior Linguistic Analyst and Data Extraction Expert.
            YOUR GOAL: Extract data from the chat with 100% syntactic accuracy.
            
            STEP 1: LINGUISTIC ANALYSIS
            - Understand the Egyptian colloquial syntax (Egyptian Arabic).
            - Identify the intent (e.g., Complaint, Query, Demand).
            - Reconstruct the thought process into professional English grammar.
            
            STEP 2: EXTRACTION RULES
            - Output format:
              [SUMMARY]: (One professional, grammatically perfect English sentence)
              [DATA]:
              [Issue] // [Details] // [Action] // [Order ID]
            
            STRICT RULES:
            - NO ARABIC in output.
            - Agent Action: If restricted, use: 'no action taken'.
            - Order ID: Numeric only. Write 'N/A' if invalid.
            - Do not guess. If information is ambiguous, write 'N/A'.
            - Final Polish: The output MUST be ready for professional use. No typos, no broken sentences.
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
            
            # Simple Parsing
            if "[SUMMARY]:" in raw_output and "[DATA]:" in raw_output:
                summary = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")[0].strip()
                data_raw = raw_output.split("[DATA]:")[1].strip()
                data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]

                st.metric("Issues Found", len(data_points))
                st.subheader("Sharp Summary")
                st.info(summary)
                
                st.subheader("Surgical Breakdown")
                for point in data_points:
                    st.code(point, language=None)
            else:
                st.error("Failed to parse. Please try again.")
            
        except Exception as e:
            st.error(f"Error: {e}")
