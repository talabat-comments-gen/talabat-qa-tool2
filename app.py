import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat QA Engine", layout="centered")
st.title("🚀 Talabat QA Analysis Engine")

# قراءة المفتاح
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

if st.button("Generate Analysis"):
    if chat_input:
        with st.spinner('Analyzing...'):
            try:
                # هذا هو الـ Prompt الصارم الذي يمنع أي تجويد
                system_prompt = f"""
                You are a professional Talabat QA assistant. 
                Analyze the chat transcript and provide a summary following this exact format:
                CST: [Issue] // Agent: [Actions] // Status: [Final Result]
                
                Rules:
                1. Differentiate clearly between CST (Customer) actions and Agent actions.
                2. Use ONLY the provided list of abbreviations.
                3. DO NOT add conversational filler, introductions, or explanations. 
                4. Be concise and accurate.
                
                Provided Abbreviations: 
                CST: Customer, RST: Restaurant, WDT: Within Delivery Time, RNA: Not Answering, FU: Follow Up, OTW: On The Way, ROP: Restaurant Operator, SLA: Service Level Agreement, ASAP: ASAP, Info: Informed, TC: Talabat Credit, ETA: ETA, R&V: Refund & Validation, OT: Offline Ticket, T&C: Terms & Condition, SPV: Supervisor, TL: Team Leader, SME: SME, VP: Vendor Portal, PDT: Promise Delivery Time, PIC: Picture, SS: Screenshot, Ven: Vendor, Comp: Compensation, WFA: Waiting For Answer, OSU: Referring to R&V, EDT: Exceeded Delivery Time, NFA: No further action, NAT: No action taken, NFAT: No further action taken, Bot: Chatbot, SOP: SOP, HVC: High-Value Customer, App: Application, CNA: Customer Not Answering, BOA: Backoffice, Min: Minute, CBH: Customer Bad History, CGH: Customer Good History, Msg: Message, Under Prep: Under Preparation, Dr: Doctor, H: Hour, HC: Hero Care, BRB: Be Right Back, PR: Partial Refund, FR: Full Refund, T2: Tier 2, T3: Tier 3, ANS: Answered, Num: Number, SMS: SMS, Acc: Account, RM: Rider Manager, AM: Account Manager, MCB: Manager Call Back, BL: Backlog.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze this chat: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.1 # قللنا الحرارة عشان الموديل يكون دقيق جداً وما يجودش
                )
                
                st.success("Analysis Complete!")
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
