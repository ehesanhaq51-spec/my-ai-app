import streamlit as st
import google.generativeai as genai

# আপনার সঠিক API Key
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"

# গুগল এআই কনফিগারেশন
try:
    genai.configure(api_key=API_KEY)
    # লেটেস্ট ফ্ল্যাশ মডেল ব্যবহার করছি যা টেক্সট ও অংকে সেরা
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Config error: {e}")

st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")
st.write("আমি এখন আপনার অংক, ফিজিক্স, কেমিস্ট্রি এবং যেকোনো প্রশ্নের উত্তর দিতে তৈরি!")

# ইনপুট বক্স খালি করার সিস্টেম
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def handle_input():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""

# টেক্সট ইনপুট (এন্টার দিলেই লেখা মুছে যাবে)
st.text_input("আপনার প্রশ্নটি এখানে লিখুন:", key="widget", on_change=handle_input)

# প্রসেসিং
if st.session_state.user_input:
    query = st.session_state.user_input
    with st.spinner('AI ভাবছে...'):
        try:
            # ইনস্ট্রাকশন সেট করে দেওয়া হচ্ছে
            prompt = f"সহজ বাংলা এবং প্রয়োজনে ইংরেজিতে উত্তর দাও। কঠিন অংক বা বিজ্ঞানের সমস্যার সমাধান স্টেপ-বাই-স্টেপ বুঝিয়ে বলো। প্রশ্ন: {query}"
            response = model.generate_content(prompt)
            
            st.write("---")
            st.markdown(response.text)
            # উত্তর দেখানোর পর প্রশ্নটি মেমোরি থেকে মুছে ফেলা
            st.session_state.user_input = ""
        except Exception as e:
            st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e}")
            st.info("টিপস: গুগল এআই স্টুডিওতে গিয়ে দেখুন আপনার API Key-টি 'Active' আছে কি না।")

st.button("Send 📤")
