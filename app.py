import streamlit as st
import google.generativeai as genai

# আপনার কি-টি আমি এখানে আবার বসিয়ে দিচ্ছি, সাবধানে চেক করবেন
API_KEY = "AIzaSyCXIudvujq26EPUcEAVmisQNNTCNFlQ-Ak"

# গুগল কনফিগারেশন
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config error: {e}")

st.set_page_config(page_title="Ehesan's AI Master", page_icon="🤖")
st.title("🤖 Ehesan's Smart AI Assistant")

user_input = st.text_input("আপনার অংক বা প্রশ্নটি এখানে লিখুন:")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('গুগল থেকে উত্তর আনা হচ্ছে...'):
            try:
                response = model.generate_content(user_input)
                st.write("---")
                st.markdown(response.text)
            except Exception as e:
                # যদি কী-তে সমস্যা থাকে তবে এখানে আসল কারণ দেখাবে
                st.error(f"গুগল বলছে: {e}")
                st.info("টিপস: গুগল এআই স্টুডিওতে গিয়ে নতুন একটি API Key তৈরি করে দেখতে পারেন।")
    else:
        st.warning("আগে কিছু লিখুন ভাই!")
