import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

st.markdown("""
    <style>
    :root { --talabat-orange: #FF7800; }
    .stButton>button { background-color: var(--talabat-orange) !important; color: white !important; border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Comprehensive Drive Map
DRIVE_MAP = [
    "Complaint about short delay (0-10 mins)", "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)", "Complaint about extreme delay (+30 mins)",
    "Follow up on existing case", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Positive", "Negative"
]

# 3. State
if "summary" not in st.session_state: st.session_state.summary = ""
if "comment" not in st.session_state: st.session_state.comment = ""

# 4. Header
st.title("🍔 Talabat Log Tool")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. UI Input
chat_input = st.text_area("Paste Transcript or Context:", height=150)
selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_MAP)

if st.button("🚀 Generate Log (Strict Format)"):
    if chat_input:
        with st.spinner('Generating log...'):
            
            # الـ Prompt ده بيجبر الـ AI يتبع الـ Template اللي بعتهولي بالظبط
            prompt = f"""
            You are a Senior Talabat Agent. Analyze the transcript/summary and generate a log.
            
            CONTACT DRIVE: {selected_drive}
            
            INSTRUCTIONS:
            1. Write a professional SUMMARY in the [SUMMARY] section.
            2. Write a technical COMMENT in the [COMMENT] section.
            
            COMMENT FORMAT (STRICT):
            {selected_drive} // asper last comment ((OT // green // asper last comment //////// "[Detailed CST message/reason]", "+++comment [Action taken by agent]", //////// [Next steps/Action] )) // [Outcome/Satisfaction] // [Next Steps] // [Info Channel]
            
            RULES:
            - DO NOT change the slashes (//) or the nested parentheses (( )) format.
            - Keep the "asper last comment" text exactly as requested.
            - Ensure the content within brackets/quotes reflects the provided transcript/summary.
            - No Arabic.
            - Use abbreviations (CST, RST, RNA, OT, TGO, TMP).
            
            Output format:
            [SUMMARY]
            ...
            [COMMENT]
            ...
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.2 # Temperature منخفض لضمان الالتزام بالـ Format
                )
                raw_text = response.choices[0].message.content
                
                # Parsing
                sum_match = re.search(r'\[SUMMARY\](.*?)\[COMMENT\]', raw_text, re.DOTALL)
                com_match = re.search(r'\[COMMENT\](.*)', raw_text, re.DOTALL)
                
                st.session_state.summary = sum_match.group(1).strip() if sum_match else "Could not parse summary."
                st.session_state.comment = com_match.group(1).strip() if com_match else raw_text
                
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Display Result
if st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Strict Comment Log"])
    with tab1: st.write(st.session_state.summary)
    with tab2: st.code(st.session_state.comment, language=None) # Code block عشان يفضل الـ format واضح
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.comment = ""
        st.rerun()
