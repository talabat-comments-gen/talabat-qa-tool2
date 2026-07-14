import streamlit as st
import os
import re
import groq # عشان نستخدم استثناءات المكتبة
from groq import Groq

# ... (باقي الكود زي ما هو)

if st.button("Generate Variations"):
    if chat_input:
        st.session_state.voted = False
        with st.spinner('Analyzing...'):
            memory_str = "\n".join(st.session_state.golden_examples)
            
            prompt = f"""...""" # (الـ Prompt بتاعك)

            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                    model="llama-3.3-70b-versatile", # لو فضلت المشكلة، غيرها لـ "llama-3.1-8b-instant"
                    temperature=0.0
                )
                st.session_state.raw_response = response.choices[0].message.content
            
            except groq.RateLimitError:
                st.error("⚠️ Rate Limit Hit! الـ API تعب، استنى 30 ثانية وجرب تاني.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ... (باقي الكود)
