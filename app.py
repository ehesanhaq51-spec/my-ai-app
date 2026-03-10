import streamlit as st
import google.generativeai as genai

# আপনার নতুন API Key
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"

# গুগল এআই কনফিগারেশন
genai.configure(api_key=API_KEY)

# ইন্টারফেস ডিজাইন
st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")
st.write("এখন আমি আপনার অংক এবং সব প্রশ্নের উত্তর দিতে পারব!")

# ইনপুট বক্স
user_input = st.text_input("আপনার অংক বা প্রশ্নটি এখানে লিখুন:", placeholder="যেমন: 5+5=?")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('AI উত্তর তৈরি করছে...'):
            try:
                # এখানে আমরা একদম লেটেস্ট ভার্সন সরাসরি কল করছি
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(user_input)
                
                st.write("---")
                if response.text:
                    st.markdown(response.text)
                else:
                    st.error("গুগল থেকে উত্তর আসেনি।")
            except Exception as e:
                # যদি উপরেরটা কাজ না করে তবে একদম বেসিক ভার্সন ট্রাই করবে
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e2}")
    else:
        st.warning("আগে কিছু লিখুন!")
