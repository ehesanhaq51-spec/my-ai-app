import streamlit as st
import google.generativeai as genai

# আপনার লেটেস্ট API Key
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"

# গুগল এআই কনফিগারেশন
genai.configure(api_key=API_KEY)

# ইন্টারফেস ডিজাইন
st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")
st.write("এখন আমি অংক এবং যেকোনো প্রশ্নের উত্তর দিতে পুরোপুরি তৈরি!")

# ইনপুট বক্স
user_input = st.text_input("আপনার অংক বা প্রশ্নটি এখানে লিখুন:", placeholder="যেমন: 5+5=?")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('AI উত্তর তৈরি করছে...'):
            try:
                # এখানে আমরা একদম লেটেস্ট 'gemini-1.5-flash' ব্যবহার করছি
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_input)
                
                st.write("---")
                if response.text:
                    st.markdown(response.text)
                else:
                    st.error("গুগল থেকে কোনো টেক্সট আসেনি।")
            except Exception as e:
                # যদি ফ্ল্যাশ মডেল কাজ না করে তবে প্রো মডেল ট্রাই করবে
                try:
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e2}")
    else:
        st.warning("আগে কিছু লিখুন!")
