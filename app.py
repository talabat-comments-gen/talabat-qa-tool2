import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Talabat Log Tool", layout="centered")

# 2. Comprehensive Contact Drives (All types)
DRIVE_LIST = [
    "Follow up on existing case", "Contactless delivery feature inquiry", "Payment method inquiry",
    "Partner related inquiry", "Rider related inquiry", "Delivery area/fee inquiry",
    "Promotions and deals inquiry", "Non-live order inquiry", "Loyalty program inquiry",
    "Work with us", "Logistics as a service inquiry", "Positive", "Negative",
    "Spam / Irrelevant", "Silent Chats", "Menu price discrepancy", "Mistake on menu",
    "Complaint about short delay (0-10 mins)", "Complaint about moderate delay (11-20 mins)",
    "Complaint about severe delay (21-30 mins)", "Complaint about extreme delay (+30 mins)"
]

# 3. UI
st.title("🍔 Talabat Log Tool (Strict)")
chat_input = st.text_area("Paste Chat Transcript:", height=150)
selected_drive = st.selectbox("Select Contact Drive:", options=DRIVE_LIST)

if st.button("🚀 Generate Strict Log"):
    if chat_input:
        with st.spinner('Generating...'):
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            
            # البرومبت صارم جداً ومحرم فيه أي رغي
            prompt = f"""
            You are a strict Talabat Log Generator. Analyze the transcript for the Contact Drive: {selected_drive}.
            
            OUTPUT FORMAT (MUST FOLLOW THIS EXACTLY):
            SUMMARY: [One single sentence summary of the issue]
            LOG: [Context/Issue] // [Action 1] // [Action 2] // [Resolution/Comp] // [Outcome]
            
            RULES:
            1. No greetings, no endings, no "Happy to help", no "Dear customer", no survey mentions.
            2. Use strictly this structure: [Issue] // [Action] // [Action] // [Res] // [Outcome].
            3. Use technical abbreviations (CST, RST, OT, comp, cst info).
            4. No Arabic in the output (English only).
            5. If no compensation, end at Resolution.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.1-8b-instant", temperature=0.1 # الحرارة منخفضة جداً عشان ميبدعش
                )
                output = response.choices[0].message.content
                st.session_state.final_output = output
            except Exception as e:
                st.error(f"Error: {e}")

if "final_output" in st.session_state:
    st.text_area("Result:", value=st.session_state.final_output, height=150)
    if st.button("🔄 Reset"):
        del st.session_state.final_output
        st.rerun()
