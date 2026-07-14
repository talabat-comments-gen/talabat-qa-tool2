import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v23", layout="centered")

if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "selected_result" not in st.session_state: st.session_state.selected_result = ""
if "voted" not in st.session_state: st.session_state.voted = False

st.title("🚀 Surgical Pro v23")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Input
chat_input = st.text_area("Paste chat transcript:", height=150)
contact_drive = st.text_input("Contact Drive:")

if st.button("Generate 4 Variations"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Analyzing...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            Memory: {memory_str}
            CONTACT DRIVE: {contact_drive if contact_drive else "General Inquiry"}
            
            Format:
            [OPTION_A]
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action] // [Order ID]
            
            [OPTION_B]
            ...
            
            (Repeat for C and D)
            
            STRICT RULES:
            - NO UNCLEAR section.
            - NO ARABIC.
            - Use abbreviations (CST, RST, RNA).
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                model="llama-3.3-70b-versatile", temperature=0.0
            )
            st.session_state.raw_response = response.choices[0].message.content

# 2. Robust Parsing
if "raw_response" in st.session_state:
    raw = st.session_state.raw_response
    options = {}
    
    # محاولة ذكية للتقطيع بدون كراش
    found_any = False
    for opt in ["A", "B", "C", "D"]:
        tag = f"[OPTION_{opt}]"
        if tag in raw:
            try:
                # قص الجزء الخاص بالخيار ده
                part = raw.split(tag)[1]
                # تنظيف من التاغ اللي بعده
                for next_opt in ["A", "B", "C", "D"]:
                    if f"[OPTION_{next_opt}]" in part:
                        part = part.split(f"[OPTION_{next_opt}]")[0]
                options[opt] = part.strip()
                found_any = True
            except:
                options[opt] = "Parsing error for this section."
        else:
            options[opt] = None

    if not found_any:
        st.error("AI output format mismatch. Raw output:")
        st.code(raw)
    else:
        # عرض النتائج
        if not st.session_state.voted:
            for opt, content in options.items():
                if content:
                    st.subheader(f"Option {opt}")
                    st.code(content, language=None)
                    if st.button(f"✅ Vote & Select Option {opt}"):
                        st.session_state.selected_result = content
                        st.session_state.golden_examples.append(content)
                        st.session_state.voted = True
                        st.rerun()
        else:
            st.success("🎉 Thanks for your feedback!")
            if st.button("🔄 Reset"):
                st.session_state.voted = False
                st.rerun()

if st.session_state.selected_result and st.session_state.voted:
    st.divider()
    st.subheader("Final Selected Report")
    st.code(st.session_state.selected_result, language=None)
