import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Talabat Log Engine", layout="centered")
st.title("🚀 Talabat Log Engine")

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
        with st.spinner('Extracting facts...'):
            try:
                # الـ Prompt ده هيمنعه يكتب كلمة واحدة زيادة عن اللي حصل
                system_prompt = """
                You are a Transcription Machine. 
                DO NOT summarize. DO NOT infer procedures. DO NOT add steps that did not happen in the chat.
                Extract facts ONLY. 
                Output format must be exactly:
                CST: [Customer Issue as written in chat] // Agent: [My specific response/action as written in chat] // Status: [Current final state]
                
                Rules:
                1. If I did not take an action, write 'NAT'.
                2. Use the provided abbreviations.
                3. If the info is missing, write 'N/A'.
                4. No polite phrases, no introductions, no explanations.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Transcript: {chat_input}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.0
                )
                
                st.code(chat_completion.choices[0].message.content, language=None)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
    else:
        st.warning("Please paste the chat transcript first.")
