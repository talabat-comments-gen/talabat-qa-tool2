import streamlit as st
import os
import json
from groq import Groq

# 1. Memory Management
EXAMPLES_FILE = "golden_examples.json"

def load_examples():
    if os.path.exists(EXAMPLES_FILE):
        with open(EXAMPLES_FILE, "r") as f:
            return json.load(f)
    return []

def save_example(issue, details, action, order_id):
    examples = load_examples()
    examples.append({"issue": issue, "details": details, "action": action, "order_id": order_id})
    # Keep only last 5 examples to avoid prompt overflow
    with open(EXAMPLES_FILE, "w") as f:
        json.dump(examples[-5:], f)
    st.success("Example saved to Golden Memory!")

# 2. Config & UI
st.set_page_config(page_title="Talabat Surgical Pro v11", layout="centered")
st.title("🚀 Talabat Surgical Pro v11 (Learning)")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

chat_input = st.text_area("Paste chat transcript here:", height=200)

if st.button("Generate & Analyze"):
    if chat_input:
        with st.spinner('Analyzing...'):
            # Load memory
            memory = load_examples()
            memory_str = "\n".join([f"{ex['issue']} // {ex['details']} // {ex['action']} // {ex['order_id']}" for ex in memory])
            
            system_prompt = f"""
            You are a Senior Talabat Agent.
            
            GOLDEN EXAMPLES (Follow this exact format and style):
            {memory_str}
            
            YOUR MISSION:
            1. Write a Sharp Summary.
            2. Extract data into lines: [Issue] // [Details] // [Action] // [Order ID].
            3. Use the style from the GOLDEN EXAMPLES provided above.
            
            STRICT RULES:
            - NO ARABIC.
            - If details are unclear, use [UNCLEAR].
            """

            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Transcript: {chat_input}"}],
                model="llama-3.3-70b-versatile",
                temperature=0.0
            )
            
            raw_output = chat_completion.choices[0].message.content
            # (Parsing logic same as before...)
            
            # Display with buttons
            # في اللوب بتاع عرض البيانات ضيف الزرار ده:
            # if st.button(f"Save as Correct", key=point):
            #     save_example(issue, details, action, order_id)
