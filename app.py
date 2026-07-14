import streamlit as st
import os
from groq import Groq

# 1. Page Config & Professional Branding
st.set_page_config(page_title="Talabat Comment Generator", layout="centered")

# Custom CSS for Animation, Talabat Colors, and Dynamic Dark/Light Support
st.markdown("""
    <style>
    /* Talabat Orange */
    :root {
        --primary-color: #FF8500;
    }
    .stButton>button { 
        background-color: var(--primary-color) !important; 
        color: white !important; 
        font-weight: bold; 
        border-radius: 8px !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Animation for Results */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-result {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Ensure font colors adapt to Dark/Light mode */
    .stCodeBlock { color: var(--text-color) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Talabat comment tool")

# 2. API setup
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Extract Data (Generate)"):
    if chat_input:
        with st.spinner('Translating & Analyzing...'):
            try:
                system_prompt = """
                You are a Literal Translation and Data Extraction Engine for Talabat.
                
                YOUR MISSION:
                1. Read the chat.
                2. Sharp Summary: Write one single, punchy, professional sentence summarizing the issue in English.
                3. Extract Data: Identify 4 distinct, non-repetitive data points.
                
                STRICT RULES:
                - Output format:
                  [SUMMARY]: (One professional English sentence)
                  [DATA]:
                  [Issue] // [Details] // [Action] // [Order ID]
                
                - SYSTEM LOGIC: If agent is restricted, ALWAYS write: 'no action taken'.
                - TRANSLATION: Literal translation (word-for-word accuracy) from Arabic to English. NO ARABIC in output.
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
                if "[SUMMARY]:" in raw_output:
                    parts = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")
                    summary = parts[0].strip()
                    data_raw = parts[1].strip()
                    data_points = [line.strip() for line in data_raw.split('\n') if line.strip()]

                # UI: Metric Counter
                col1, col2 = st.columns([1, 3])
                col1.metric("Issues", len(data_points))
                
                # UI: Sharp Summary
                st.subheader("Sharp Summary")
                st.info(summary)
                
                # UI: Data Points with Animation
                st.subheader("Extracted Details")
                st.markdown('<div class="animated-result">', unsafe_allow_html=True)
                for point in data_points:
                    st.code(point, language=None)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please paste the chat transcript.")
