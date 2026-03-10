import streamlit as st
import google.generativeai as genai

# পেজ সেটআপ
st.set_page_config(page_title="Ehesan's Pro AI", page_icon="🚀")
st.title("🚀 Ehesan's Smart AI Assistant")
st.write("যেকোনো প্রশ্ন বা অংক লিখুন, আমি উত্তর দিচ্ছি!")

# আপনার API Key এখানে দিন (অবশ্যই aistudio.google.com থেকে কি-টি নিয়ে বসাবেন)
API_KEY = "আপনার_API_KEY_এখানে_দিন" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ইনপুট বক্স
user_input = st.text_input("এখানে লিখুন:", placeholder="Ask me anything...")

# সুন্দর একটি 'Send' বাটন যোগ করা
if st.button("Send 📤"):
    if user_input:
        with st.spinner('AI উত্তর খুঁজছে...'):
            try:
                response = model.generate_content(user_input)
                st.success("উত্তর পেয়েছি!")
                st.markdown(f"**AI:** \n\n {response.text}")
            except Exception as e:
                st.error("API Key বসানো হয়নি অথবা কোনো ভুল হয়েছে।")
    else:
        st.warning("আগে কিছু লিখুন ভাই!")
