import streamlit as st
import os
from groq import Groq

# 1. Page Config & Talabat Branding (CSS)
st.set_page_config(page_title="Talabat Intelligence", layout="centered")

st.markdown("""
    <style>
    /* Talabat Orange Theme */
    .stButton>button { background-color: #FF8500 !important; color: white !important; font-weight: bold; border: none; }
    h1 { color: #FF8500; }
    .stApp { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat Surgical Dashboard")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate Intelligence Report"):
    if chat_input:
        with st.spinner('Performing deep analysis...'):
            try:
                system_prompt = """
                You are a Talabat Data Intelligence Unit.
                
                YOUR MISSION:
                1. Read the chat.
                2. Sharp Summary: Write one single, punchy, professional sentence summarizing the entire issue in English.
                3. Extract Data: Identify 4 distinct, non-repetitive data points.
                
                STRICT RULES:
                - Output format:
                  [SUMMARY]: (Your sharp summary here)
                  [DATA]:
                  [Issue] // [Details] // [Action] // [Order ID]
                
                - SYSTEM LOGIC: If the agent is restricted, ALWAYS write: 'no action taken'.
                - TRANSLATION: Literal translation from Arabic to English. NO ARABIC in output.
                - Order ID: Purely numeric. If invalid, 'N/A'.
                - NO filler, NO headers other than [SUMMARY] and [DATA].
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
                
                # Parsing Logic
                summary = ""
                data_points = []
                
                if "[SUMMARY]:" in raw_output:
                    summary = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")[0].strip()
                    data_raw = raw_output.split("[DATA]:")[1].strip()
                    data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]

                # Displaying Metrics
                col1, col2 = st.columns(2)
                col1.metric("Issues Extracted", len(data_points))
                
                # Display Summary
                st.subheader("Sharp Summary")
                st.info(summary)
                
                # Display Data Points
                st.subheader("Detailed Breakdown")
                for point in data_points:
                    st.code(point, language=None)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste the transcript.")
