import streamlit as st
import os
from groq import Groq

# 1. Config
st.set_page_config(page_title="Surgical Pro v16", layout="centered")

if "golden_examples" not in st.session_state: st.session_state.golden_examples = []
if "selected_result" not in st.session_state: st.session_state.selected_result = ""

st.title("🚀 Surgical Pro v16")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript:", height=150)

if st.button("Generate 4 Variations"):
    if chat_input:
        with st.spinner('Thinking...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            # أمر صريح بإلغاء UNCLEAR وإنتاج 4 خيارات
            prompt = f"""
            You are a Senior Talabat Agent. Generate FOUR distinct variations (A, B, C, D).
            
            Memory (Use this style): {memory_str}
            
            Format for each:
            [OPTION_X]
            [SUMMARY]: ...
            [DATA]: [Issue] // [Details] // [Action] // [Order ID]
            
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

# 2. Display & Selection
if "raw_response" in st.session_state:
    raw = st.session_state.raw_response
    
    # تقسيم الرد لـ 4 خيارات
    options = {"A": "", "B": "", "C": "", "D": ""}
    for opt in ["A", "B", "C", "D"]:
        try:
            # تقطيع بناءً على التاجز
            part = raw.split(f"[OPTION_{opt}]")[1].split("[OPTION_")[0]
            options[opt] = part.strip()
        except:
            options[opt] = "Error generating this option."

    # عرض الخيارات تحت بعض
    for opt, content in options.items():
        st.subheader(f"Option {opt}")
        st.code(content, language=None)
        
        # الزرار تحت كل خيار
        if st.button(f"✅ Vote & Select Option {opt}"):
            st.session_state.selected_result = content
            st.session_state.golden_examples.append(content)
            st.success(f"Option {opt} selected and saved to training data!")
            st.rerun()

# 3. Final Selected Area
if st.session_state.selected_result:
    st.divider()
    st.subheader("Final Selected Report")
    st.code(st.session_state.selected_result, language=None)
