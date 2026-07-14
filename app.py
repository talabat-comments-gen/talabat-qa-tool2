import streamlit as st
import os
import time
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Surgical Pro v10", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v10 (Robust)")

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
        with st.spinner('Analyzing...'):
            try:
                system_prompt = """
                You are a Senior Talabat Agent. Output must be ready to copy.
                
                STRUCTURE:
                [SUMMARY]: Write a sharp, professional summary.
                [DATA]: List lines in format: [Issue] // [Details] // [Action] // [Order ID].
                [UNCLEAR]: If something is missing or unclear, list it here.
                
                RULES:
                - Use abbreviations: CST, RST, RNA, NAT, etc.
                - NO ARABIC.
                - If the AI fails to generate tags, at least format the data lines clearly.
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
                st.subheader("Sharp Summary")
                
                # Logic: Try to split by tags, if fails, display raw text
                if "[SUMMARY]:" in raw_output:
                    # Extraction logic
                    parts = raw_output.split("[SUMMARY]:")[1]
                    summary = parts.split("[DATA]:")[0].strip() if "[DATA]:" in parts else "No summary found."
                    st.info(summary)
                    
                    st.subheader("Surgical Breakdown")
                    if "[DATA]:" in parts:
                        data_part = parts.split("[DATA]:")[1]
                        # Handling UNCLEAR if present
                        if "[UNCLEAR]:" in data_part:
                            data_lines = data_part.split("[UNCLEAR]:")[0].strip()
                            unclear_part = data_part.split("[UNCLEAR]:")[1].strip()
                            st.warning("⚠️ Ambiguous Sections:")
                            st.write(unclear_part)
                        else:
                            data_lines = data_part.strip()
                            
                        # Show Data
                        for line in data_lines.split('\n'):
                            if "//" in line:
                                st.code(line.strip(), language=None)
                else:
                    # Fallback if tags are missing
                    st.warning("Tags missing, but here is the raw output:")
                    st.text(raw_output)
                    
            except Exception as e:
                st.error(f"Error: {e}")
