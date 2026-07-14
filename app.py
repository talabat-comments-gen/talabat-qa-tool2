import streamlit as st
import os
import time
from groq import Groq

# 1. Config & UI
st.set_page_config(page_title="Talabat Surgical Pro v6", layout="centered")
st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v6")

# 2. Abbreviations Glossary
abbreviations = {
    "CST": "Customer", "RST": "Restaurant", "RNA": "Restaurant/Rider Not Answering",
    "FU": "Follow Up", "OTW": "On The Way", "NAT": "No action taken",
    "T&C": "Terms & Condition", "SPV": "Supervisor", "TC": "Talabat Credit",
    "ETA": "Estimated Time Arrival", "R&V": "Refund & Validation", "Info": "Informed",
    "CNA": "Customer Not Answering", "PR": "Partial Refund", "FR": "Full Refund"
}

with st.expander("📚 Abbreviations Glossary (Use these in output)"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Extract Data (Perfect Formatting)"):
    if chat_input:
        with st.spinner('Linguistic Analysis...'):
            # 5-second countdown
            progress_bar = st.progress(0)
            for i in range(5):
                time.sleep(1)
                progress_bar.progress((i + 1) * 20)
            
            try:
                system_prompt = """
                You are a Senior Data Extraction Expert for Talabat.
                
                YOUR MISSION:
                1. Write a Sharp Summary (one professional sentence).
                2. Extract data into lines with this EXACT format: 
                   [Issue] // [Details] // [Action] // [Order ID]
                
                STRICT RULES:
                - Use the provided abbreviations (CST, RST, RNA, NAT, etc.) in the output.
                - Linguistic Accuracy: If the customer provides clarification, capture it clearly. If they complain, capture the issue.
                - DO NOT classify intents as headers. Just output the lines.
                - System Logic: If the agent is restricted, use 'no action taken' (or NAT).
                - NO ARABIC. English only.
                - Precision: 200%. Do not summarize the [Details] too much; keep the customer's specific explanation.
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
                
                # Logic to split summary and data
                summary = "Summary not generated."
                data_points = []
                
                if "[SUMMARY]:" in raw_output:
                    parts = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")
                    summary = parts[0].strip()
                    if len(parts) > 1:
                        data_raw = parts[1].strip()
                        data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]

                # Display Results
                st.subheader("Sharp Summary")
                st.info(summary)
                
                st.subheader("Surgical Breakdown")
                st.metric("Issues Extracted", len(data_points))
                
                for point in data_points:
                    st.code(point, language=None)
            
            except Exception as e:
                st.error(f"Error: {e}")
