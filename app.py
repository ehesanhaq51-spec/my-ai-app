import streamlit as st
import google.generativeai as genai

# আপনার নতুন API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# কনফিগারেশন এবং সেফটি চেক
try:
    genai.configure(api_key=API_KEY)
    # আপনার একাউন্টে কোন মডেলটি ভালো কাজ করে তা নিজে খুঁজে বের করবে
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config error: {e}")

st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")

# বক্স খালি করার জন্য সেশন স্টেট
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def handle_input():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""

# ইনপুট বক্স (প্রশ্ন লিখে এন্টার দিলে লেখাটি ভ্যানিশ হয়ে যাবে)
st.text_input("আপনার অংক বা যেকোনো প্রশ্ন এখানে লিখুন:", key="widget", on_change=handle_input)

# প্রসেসিং পার্ট
if st.session_state.user_input:
    query = st.session_state.user_input
    with st.spinner('AI ভাবছে...'):
        try:
            # ইনস্ট্রাকশন: সে যেন আমার (Gemini) মতো বুদ্ধিমান হয়
            instruction = (
                "You are an expert tutor like Gemini. Solve Math, Physics, and Chemistry "
                "problems step-by-step in Bengali. Always respond in Bengali. "
                "Be polite and helpful."
            )
            response = model.generate_content(f"{instruction}\n\nQuestion: {query}")
            
            st.write(f"**প্রশ্ন:** {query}")
            st.write("---")
            st.markdown(response.text)
            
            # মেমোরি ক্লিয়ার করা
            st.session_state.user_input = ""
        except Exception as e:
            st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e}")
            st.info("টিপস: গুগল এআই স্টুডিওতে আপনার কোটা শেষ হয়েছে কি না একবার চেক করুন।")

st.button("Send 📤")
