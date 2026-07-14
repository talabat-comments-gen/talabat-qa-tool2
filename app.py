import streamlit as st
import os
import re
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

# 2. Comprehensive Drive Map
DRIVE_MAP = [
    "Complaint about late order", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Missing item / Wrong item", "Delivery area/fee inquiry",
    "Negative feedback", "Positive feedback", "Order tracking issue"
]

# 3. UI
st.title("🍔 Talabat Log Tool (Summary + Log)")
st.markdown("---")

chat_input = st.text_area("Paste Transcript / Details:", height=150)
selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_MAP)

if st.button("🚀 Generate Log"):
    if chat_input:
        with st.spinner('Writing Summary & Log...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            # البرومبت يطلب جزئين منفصلين بوضوح
            prompt = f"""
            You are a professional Talabat agent. Analyze the transcript for: {selected_drive}.
            
            Provide the output in TWO separate sections, strictly labeled as follows:
            
            SUMMARY:
            [Write one clear sentence summarizing the customer's main issue]
            
            LOG:
            [Issue/Context] // [Action 1] // [Action 2] // [Resolution/Comp] // [Outcome/Status]
            
            RULES:
            1. NO greetings, NO endings, NO survey mentions, NO "Dear customer".
            2. Use technical abbreviations (CST, RST, comp, OT, TGO, TMP).
            3. Be factual, concise, and professional.
            4. If no compensation was given, skip the comp part.
            5. No Arabic words in the output.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.2
                )
                raw_text = response.choices[0].message.content
                
                # Parsing logic
                # بندور على SUMMARY و LOG عشان نفصلهم
                sum_match = re.search(r'SUMMARY:(.*?)LOG:', raw_text, re.DOTALL | re.IGNORECASE)
                log_match = re.search(r'LOG:(.*)', raw_text, re.DOTALL | re.IGNORECASE)
                
                summary = sum_match.group(1).strip() if sum_match else "N/A"
                log_result = log_match.group(1).strip() if log_match else raw_text
                
                st.session_state.summary = summary
                st.session_state.log_result = log_result
            except Exception as e:
                st.error(f"Error: {e}")

# 4. Display Result
if "summary" in st.session_state and st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Technical Log"])
    
    with tab1:
        st.info(st.session_state.summary)
        
    with tab2:
        st.code(st.session_state.log_result, language=None)
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.log_result = ""
        st.rerun()
