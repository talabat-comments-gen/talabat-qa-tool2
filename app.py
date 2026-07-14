import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

# 2. Comprehensive Drive Map (Context Only)
DRIVE_MAP = [
    "Complaint about short delay (0-10 mins)", "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)", "Complaint about extreme delay (+30 mins)",
    "Follow up on existing case", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Positive", "Negative", "Order tracking issue", "Missing item"
]

# 3. State
if "summary" not in st.session_state: st.session_state.summary = ""
if "comment" not in st.session_state: st.session_state.comment = ""

# 4. UI Input
st.title("🍔 Talabat Log Tool")
st.markdown("---")
chat_input = st.text_area("Paste Transcript / Details:", height=150)
selected_drive = st.selectbox("Select Contact Drive (For Context):", options=DRIVE_MAP)

# 5. Generation Logic
if st.button("🚀 Generate Natural Log"):
    if chat_input:
        with st.spinner('Writing professional log...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are a Senior Talabat Agent. Write a professional log based on the transcript provided.
            
            CONTACT DRIVE: {selected_drive}
            
            INSTRUCTIONS:
            1. Write a professional, concise SUMMARY in the [SUMMARY] section.
            2. Write a technical COMMENT (Log) in the [COMMENT] section.
            
            COMMENT FORMAT RULES:
            - Do NOT use fixed phrases like "asper last comment".
            - Use the following separator structure for a dense, professional look:
              Category // Status/Context // (( Actions taken, Internal checks, Compensations )) // Outcome // Next Steps // Info Channel
            - Use "(( ))" for details or sub-logs.
            - Use "////////" only if you need to separate distinct internal notes or actions.
            - Focus on: What happened? What did we do? What's the outcome?
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
                    model="llama-3.1-8b-instant", temperature=0.4
                )
                raw_text = response.choices[0].message.content
                
                sum_match = re.search(r'\[SUMMARY\](.*?)\[COMMENT\]', raw_text, re.DOTALL)
                com_match = re.search(r'\[COMMENT\](.*)', raw_text, re.DOTALL)
                
                st.session_state.summary = sum_match.group(1).strip() if sum_match else "Could not parse summary."
                st.session_state.comment = com_match.group(1).strip() if com_match else raw_text
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Display Result
if st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Professional Log"])
    with tab1: st.write(st.session_state.summary)
    with tab2: st.code(st.session_state.comment, language=None)
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.comment = ""
        st.rerun()
