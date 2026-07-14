import streamlit as st
import os
import time
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Talabat Surgical Pro v8", layout="centered")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; border-radius: 8px !important; }
    .stCodeBlock { border-left: 5px solid #FF8500 !important; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Pro v8")

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

if st.button("Generate Final Report"):
    if chat_input:
        with st.spinner('Refining Logic & Rhythm...'):
            # Progress simulation
            progress_bar = st.progress(0)
            for i in range(5):
                time.sleep(0.5)
                progress_bar.progress((i + 1) * 20)
            
            try:
                # الـ Prompt الجديد: يركز على الـ Rhythm والـ Accuracy
                system_prompt = """
                You are a Senior Talabat Agent. Your output must be ready to copy without review.
                
                RHYTHM RULES:
                1. [SUMMARY]: A single, sharp, punchy sentence. Example: "CST reported missing items from RST order and requested immediate compensation."
                2. [DATA]: Use EXACT format: [Issue] // [Details] // [Action] // [Order ID].
                
                STRICT CONSTRAINTS:
                - Use provided abbreviations (CST, RST, RNA, NAT).
                - Logic: If clarification -> state what was clarified. If complaint -> state the failure.
                - NO ARABIC.
                - If the AI fails to generate the summary or data, you have failed the mission. Be precise.
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
                summary = "System error: Failed to generate summary."
                data_points = []
                
                # إجباري الموديل يلتزم بالتاجز
                if "[SUMMARY]:" in raw_output:
                    temp = raw_output.split("[SUMMARY]:")[1]
                    if "[DATA]:" in temp:
                        summary = temp.split("[DATA]:")[0].strip()
                        data_raw = temp.split("[DATA]:")[1].strip()
                        data_points = [line.strip() for line in data_raw.split('\n') if line.strip() and "//" in line]
                    else:
                        summary = temp.strip()

                # Display
                st.subheader("Sharp Summary")
                st.info(summary)
                
                st.subheader("Surgical Breakdown")
                st.metric("Total Lines", len(data_points))
                
                for point in data_points:
                    st.code(point, language=None)
                    
            except Exception as e:
                st.error(f"Error: {e}")
