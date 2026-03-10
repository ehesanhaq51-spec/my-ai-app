import streamlit as st
from groq import Groq

# আপনার Groq API Key
client = Groq(api_key="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")

st.set_page_config(page_title="Ehesan's AI", page_icon="🚀")
st.title("🚀 Ehesan's Pro AI Assistant")

# বক্স খালি করার ফাংশন
def clear_text():
    st.session_state["user_question"] = st.session_state["input"]
    st.session_state["input"] = ""

# ইনপুট বক্স (এটার সাথে clear_text কানেক্ট করা হয়েছে)
st.text_input("আপনার প্রশ্নটি লিখুন:", key="input", on_change=clear_text)

# প্রশ্ন প্রসেস করা
if "user_question" in st.session_state and st.session_state["user_question"]:
    question = st.session_state["user_question"]
    
    with st.spinner('AI উত্তর তৈরি করছে...'):
        try:
            # এখানে আমরা AI-কে বলে দিচ্ছি সে যেন বাংলা উত্তর দেয়
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Always try to understand and reply in Bengali if the user speaks in Bengali or Romanized Bengali (Banglish)."},
                    {"role": "user", "content": question}
                ]
            )
            st.write(f"**প্রশ্ন:** {question}")
            st.write("---")
            st.markdown(completion.choices[0].message.content)
            
            # কাজ শেষ হলে প্রশ্ন মুছে ফেলা
            st.session_state["user_question"] = ""
        except Exception as e:
            st.error(f"Error: {e}")

st.button("Send 📤")
