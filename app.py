import streamlit as st
import google.generativeai as genai

# আপনার নতুন কী
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"
genai.configure(api_key=API_KEY)

st.title("Ehesan's Final Bot")

user_input = st.text_input("যেকোনো প্রশ্ন লিখুন:")
if st.button("Send"):
    try:
        # একদম সিম্পল মডেল ব্যবহার
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        st.write(response.text)
    except Exception as e:
        st.error("গুগল এখনো আপনার কী-টি অ্যাক্টিভেট করেনি। দয়া করে ১৫ মিনিট পর ট্রাই করুন।")
