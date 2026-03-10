import streamlit as st
import google.generativeai as genai

# --- এখানে আপনার চাবি বসান ---
API_KEY = "AIzaSyCXIudvujq26EPUcEAVmisQNNTCNFlQ-Ak" 

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key কাজ করছে না।")

# --- ইন্টারফেস ---
st.set_page_config(page_title="Ehesan's AI Master", page_icon="🎓")
st.title("🎓 Ehesan's Pro AI")
st.write("যেকোনো প্রশ্ন বা অংক লিখুন, আমি উত্তর দিচ্ছি!")

user_input = st.text_input("এখানে লিখুন:", placeholder="যেমন: 25 * 4 = কত?")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('উত্তর খোঁজা হচ্ছে...'):
            try:
                response = model.generate_content(user_input)
                st.write("---")
                st.markdown(f"**AI উত্তর:**\n\n{response.text}")
            except Exception as e:
                st.error("দুঃখিত, গুগল থেকে উত্তর আনতে সমস্যা হচ্ছে। কী-টি চেক করুন।")
    else:
        st.warning("আগে কিছু লিখুন!")
