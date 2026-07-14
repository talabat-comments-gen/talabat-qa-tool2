import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered", page_icon="🍔")

# 2. Comprehensive Drive Map (Context Only)
DRIVE_MAP = [
    "Complaint about short delay (0-10 mins)", "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)", "Complaint about extreme delay (+30 mins)",
    "Follow up on existing case", "Check order status", "Refunds/Wallet/Double Charge",
    "Partner related inquiry", "Positive", "Negative", "Order tracking issue", "Missing item",
    "Partner related inquiry", "Rider related inquiry", "Delivery area/fee inquiry"
]

# 3. UI Input
st.title("🍔 Talabat Log Tool (Simple & Pro)")
st.markdown("---")

chat_input = st.text_area("Paste Transcript / Details:", height=150)
selected_drive = st.selectbox("Select Contact Drive (Context):", options=DRIVE_MAP)

if st.button("🚀 Generate Simple Log"):
    if chat_input:
        with st.spinner('Writing simple & clear log...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            # التعديل هنا: تعليمات بشرية بسيطة جداً
            prompt = f"""
            You are a professional Talabat agent. Analyze the transcript based on: {selected_drive}.
            
            Write the output in TWO parts:
            1. SUMMARY: One sentence summary of the issue.
            2. COMMENT: A clear, logical log of what happened.
               - Start by stating what the customer wanted/complained about.
               - List exactly what you did (e.g., contacted restaurant, checked status, applied voucher).
               - State the result (e.g., customer satisfied).
            
            RULES:
            - Write in plain, professional English.
            - NO weird symbols, NO dense formatting, NO "asper last comment" templates.
            - Just clear, rational sentences that anyone can understand.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.4
                )
                raw_text = response.choices[0].message.content
                
                # فصل الـ Summary عن الـ Comment
                parts = raw_text.split("COMMENT:") if "COMMENT:" in raw_text else raw_text.split("COMMENT")
                summary = parts[0].replace("SUMMARY:", "").strip() if len(parts) > 0 else "N/A"
                comment = parts[1].strip() if len(parts) > 1 else raw_text
                
                st.session_state.summary = summary
                st.session_state.comment = comment
            except Exception as e:
                st.error(f"Error: {e}")

# 6. Display Result
if "summary" in st.session_state and st.session_state.summary:
    tab1, tab2 = st.tabs(["📋 Summary", "📝 Professional Log (Comment)"])
    with tab1: st.write(st.session_state.summary)
    with tab2: st.write(st.session_state.comment)
        
    if st.button("🔄 Reset"):
        st.session_state.summary = ""
        st.session_state.comment = ""
        st.rerun()
