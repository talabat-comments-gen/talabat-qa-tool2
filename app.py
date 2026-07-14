import streamlit as st
import os
import time
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Surgical Pro v9", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v9 (Clarity Engine)")

# 2. Abbreviations
abbreviations = {
    "CST": "Customer", "RST": "Restaurant", "RNA": "Restaurant/Rider Not Answering",
    "FU": "Follow Up", "OTW": "On The Way", "NAT": "No action taken",
    "T&C": "Terms & Condition", "SPV": "Supervisor", "TC": "Talabat Credit",
    "ETA": "Estimated Time Arrival", "R&V": "Refund & Validation", "Info": "Informed"
}

with st.expander("📚 Abbreviations Glossary"):
    st.table(list(abbreviations.items()))

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Final Report"):
    if chat_input:
        with st.spinner('Analyzing Ambiguities...'):
            try:
                system_prompt = """
                You are a Senior Talabat Agent. Your output must be ready to copy without review.
                
                YOUR MISSION:
                1. Write a Sharp Summary (one professional sentence).
                2. Extract data into lines with this EXACT format: [Issue] // [Details] // [Action] // [Order ID].
                3. CRITICAL: AMBIGUITY DETECTION. If any part of the chat is vague, missing details, or unclear (e.g., missing Order ID, unclear customer request), DO NOT GUESS.
                   - List such parts under a separate '[UNCLEAR]' section and explain why (e.g., "Missing Order ID", "Ambiguous request").
                
                STRICT RULES:
                - Use provided abbreviations (CST, RST, RNA, NAT).
                - NO ARABIC.
                - If the info is unclear, the [UNCLEAR] section is MANDATORY.
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
                
                # Parsing logic for 3 sections
                summary = "System error."
                data_points = []
                unclear_points = []
                
                if "[SUMMARY]:" in raw_output:
                    parts = raw_output.split("[SUMMARY]:")[1]
                    # Split logic
                    if "[DATA]:" in parts:
                        summary = parts.split("[DATA]:")[0].strip()
                        remaining = parts.split("[DATA]:")[1]
                        
                        if "[UNCLEAR]:" in remaining:
                            data_raw = remaining.split("[UNCLEAR]:")[0].strip()
                            unclear_raw = remaining.split("[UNCLEAR]:")[1].strip()
                            unclear_points = [line.strip() for line in unclear_raw.split('\n') if line.strip()]
                        else:
                            data_raw = remaining.strip()
                        
                        data_points = [line.strip() for line in data_raw.split('\n') if line.strip() and "//" in line]

                # Display
                st.subheader("Sharp Summary")
                st.info(summary)
                
                st.subheader("Surgical Breakdown")
                for point in data_points:
                    st.code(point, language=None)
                
                if unclear_points:
                    st.warning("⚠️ Ambiguous/Unclear Sections:")
                    for point in unclear_points:
                        st.error(point)
                    
            except Exception as e:
                st.error(f"Error: {e}")
