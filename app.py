import streamlit as st
import os
import time
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Surgical Pro v7", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v7 (Robust)")

# 2. Abbreviations
abbreviations = {
    "CST": "Customer", "RST": "Restaurant", "RNA": "Restaurant/Rider Not Answering",
    "FU": "Follow Up", "OTW": "On The Way", "NAT": "No action taken",
    "T&C": "Terms & Condition", "SPV": "Supervisor", "TC": "Talabat Credit",
    "ETA": "Estimated Time Arrival", "R&V": "Refund & Validation", "Info": "Informed",
    "CNA": "Customer Not Answering", "PR": "Partial Refund", "FR": "Full Refund"
}

with st.expander("📚 Abbreviations Glossary"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Extract Data (Robust Parsing)"):
    if chat_input:
        with st.spinner('Linguistic Analysis & Extraction...'):
            try:
                system_prompt = """
                You are a Senior Data Extraction Expert for Talabat.
                
                YOUR MISSION:
                1. Write a Sharp Summary (one professional sentence).
                2. Extract data into lines with this EXACT format: 
                   [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT FORMATTING:
                You MUST include '[SUMMARY]:' before your summary and '[DATA]:' before your lines.
                If you do not use these tags, the tool will fail.
                
                STRICT RULES:
                - Use abbreviations: CST, RST, RNA, NAT, etc.
                - NO ARABIC in output.
                - Precision: 200%. Capture the customer's specific explanation details perfectly.
                - Agent restricted? Use 'NAT' or 'no action taken'.
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
                
                # Robust Parsing Logic
                summary = "Summary not found in output."
                data_points = []
                
                if "[SUMMARY]:" in raw_output and "[DATA]:" in raw_output:
                    # Case 1: Perfect format
                    parts = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")
                    summary = parts[0].strip()
                    data_raw = parts[1].strip()
                    data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]
                else:
                    # Case 2: Fallback (Try to find lines anyway)
                    summary = "Format error: Tags missing. Raw output displayed below."
                    data_points = [line.strip() for line in raw_output.split('\n') if "//" in line]

                # UI
                st.subheader("Sharp Summary")
                st.info(summary)
                
                st.subheader("Surgical Breakdown")
                st.metric("Issues Extracted", len(data_points))
                
                for point in data_points:
                    st.code(point, language=None)
                    
            except Exception as e:
                st.error(f"Error: {e}")
