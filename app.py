import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat QA Engine", layout="centered")
st.title("🚀 Talabat QA Engine (Strict Mode)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

chat_input = st.text_area("Paste Chat Transcript Here:", height=400)

if st.button("Generate Log"):
    if chat_input:
        with st.spinner('Extracting data...'):
            try:
                # الـ System Prompt هنا أجبرناه يكون آلة (Data Extractor)
                system_prompt = f"""
                You are a strict data logger. Extract information from the chat and output ONLY in this exact format:
                CST: [Issue/Complaint] // [Context/Details] // [Agent Action] // [Status/Resolution]
                
                Rules:
                1. DO NOT write full sentences.
                2. Use the provided abbreviations ONLY.
                3. DO NOT add intro, outro, or explanations.
                4. Be concise and strictly follow the '//' format.
                
                Abbreviations: CST, RST, WDT, RNA, FU, OTW, ROP, SLA, ASAP, Info, TC, ETA, R&V, OT, T&C, SPV, TL, SME, VP, PDT, PIC, SS, Ven, Comp, WFA, OSU, EDT, NFA, NAT, NFAT, Bot, SOP, HVC, App, CNA, BOA, Min, CBH, CGH, Msg, Under Prep, Dr, H, HC, BRB, PR, FR, T2, T3, ANS, Num, SMS, Acc, RM, AM, MCB, BL.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Extract the log from this chat: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0  # صفر عشان يمنع التجويد تماماً
                )
                
                st.code(chat_completion.choices[0].message.content, language=None)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
