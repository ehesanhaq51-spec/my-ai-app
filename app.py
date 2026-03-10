import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার একদম নতুন API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# গুগল কনফিগারেশন
genai.configure(api_key=API_KEY)

# পেজ ডিজাইন
st.set_page_config(page_title="Ehesan's Ultimate AI", page_icon="🚀")
st.title("🚀 Ehesan's Ultimate AI Assistant")
st.write("আমি এখন টেক্সট এবং ছবি দেখে অংক ও বিজ্ঞানের সমাধান দিতে পারি!")

# সেশন স্টেট (বক্স খালি করার জন্য)
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

def clear_box():
    st.session_state.user_query = st.session_state.input_widget
    st.session_state.input_widget = ""

# ছবি আপলোড অপশন
uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি দিন", type=["jpg", "jpeg", "png"])

# টেক্সট ইনপুট
st.text_input("আপনার প্রশ্ন লিখুন:", key="input_widget", on_change=clear_box)

# বাটন বা এন্টার চাপলে প্রসেস শুরু
if st.session_state.user_query or uploaded_file:
    query = st.session_state.user_query
    with st.spinner('বিশ্লেষণ করছি...'):
        try:
            # লেটেস্ট মডেল লোড করা
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # প্রম্পট সেট করা যেন আমার (Gemini) মতো বুদ্ধিমান উত্তর দেয়
            prompt = (
                "You are a highly intelligent AI tutor like Gemini. "
                "Solve math, physics, and chemistry problems step-by-step. "
                "Always respond in clear Bengali. If a picture is provided, analyze it deeply."
            )

            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img, query if query else "Explain this image."])
            else:
                response = model.generate_content(f"{prompt} Question: {query}")
            
            st.write("---")
            st.markdown(response.text)
            
            # কাজ শেষে কুয়েরি মুছে ফেলা
            st.session_state.user_query = ""
            
        except Exception as e:
            st.error(f"দুঃখিত ভাই, এরর হয়েছে: {e}")
            st.info("টিপস: GitHub-এ ফাইল সেভ করার সময় 'Allow Secret' ক্লিক করতে ভুলবেন না।")

if uploaded_file:
    st.image(uploaded_file, caption="আপলোড করা ছবি", use_container_width=True)
