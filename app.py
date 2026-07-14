import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Surgical Pro v12", layout="wide")

st.markdown("""
    <style>
    :root { --primary-color: #FF8500; }
    .stButton>button { background-color: var(--primary-color) !important; color: white !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Development Tools
with st.sidebar:
    st.header("🛠️ Dev Tools")
    show_raw = st.checkbox("Show Raw Output (Debugging)", value=False)
    st.divider()
    st.caption("Instructions: If output is wrong, check 'Raw Output' to see if the AI hallucinated.")

st.title("🚀 Talabat Surgical Pro v12")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=150)

if st.button("Generate & Separate"):
    if chat_input:
        with st.spinner('Processing...'):
            try:
                system_prompt = """
                You are a Senior Talabat Agent.
                [SUMMARY]: One sharp professional sentence.
                [DATA]: Lines format: [Issue] // [Details] // [Action] // [Order ID].
                [UNCLEAR]: If something is vague.
                Rules: NO ARABIC. Use abbreviations (CST, RST).
                """

                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.3-70b-versatile", temperature=0.0
                )
                raw_output = response.choices[0].message.content
                
                # Dev Tool: Show Raw
                if show_raw:
                    st.subheader("Raw Output (Dev Mode)")
                    st.text(raw_output)

                # Parsing
                summary = "N/A"
                data_points = []
                
                if "[SUMMARY]:" in raw_output:
                    summary = raw_output.split("[SUMMARY]:")[1].split("[DATA]:")[0].strip()
                
                if "[DATA]:" in raw_output:
                    data_block = raw_output.split("[DATA]:")[1].split("[UNCLEAR]:")[0] if "[UNCLEAR]:" in raw_output else raw_output.split("[DATA]:")[1]
                    data_points = [line.strip() for line in data_block.split('\n') if "//" in line]

                # UI: Sharp Summary
                st.subheader("Sharp Summary")
                st.info(summary)
                
                # UI: Data Points with "Zoom" & "Copy"
                st.subheader("Surgical Data Points")
                for i, point in enumerate(data_points):
                    with st.expander(f"Data Point {i+1}: {point.split('//')[0][:30]}...", expanded=True):
                        st.code(point, language=None)
                        st.caption("Use the copy button in the top-right of the code block above.")

            except Exception as e:
                st.error(f"Development Error: {e}")
