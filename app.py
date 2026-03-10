import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার একদম নতুন এবং সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# অটো-মডেল সিলেকশন এবং কনফিগারেশন
try:
    genai.configure(api_key=API_KEY)
    # আপনার চাবির আন্ডারে যে মডেলগুলো এখন কাজ করছে সেগুলো খুঁজে বের করা
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # সবচেয়ে লেটেস্টটা বেছে নেওয়া (Gemini 1.5 Flash থাকলে সেটা আগে নিবে)
    selected_model = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    model = genai.GenerativeModel(selected_model)
except Exception as e:
    st.error(f"API সংযোগে সমস্যা: {e}")

st.set_page_config(page_title="Ehesan's Pro AI Master", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Master")

# বক্স খালি করার জন্য সেশন স্টেট
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

def clear_input():
    st.session_state.user_query = st.session_state.widget
    st.session_state.widget = ""

# ইমেজ আপলোডার (চোখের কাজ করবে)
uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি আপলোড করুন", type=["jpg", "jpeg", "png"])

# টেক্সট ইনপুট (মগজের কাজ করবে)
st.text_input("আপনার প্রশ্নটি লিখুন:", key="widget", on_change=clear_input)

# প্রসেসিং
if st.session_state.user_query or uploaded_file:
    query = st.session_state.user_query
    with st.spinner('মাস্টারমাইন AI বিশ্লেষণ করছে...'):
        try:
            # ইনস্ট্রাকশন: ঠিক আমার মতো করে উত্তর দিতে বলা হয়েছে
            instruction = (
                "You are an expert tutor like Gemini. Solve any Math, Physics, or "
                "Chemistry problems step-by-step in Bengali. Always respond in clear Bengali. "
                "Be detailed and easy to understand."
            )
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([instruction, img, query if query else "Explain this picture."])
            else:
                response = model.generate_content(f"{instruction}\n\nQuestion: {query}")
            
            st.write("---")
            st.markdown(response.text)
            st.session_state.user_query = "" # কাজ শেষে কুয়েরি মুছে ফেলা
            
        except Exception as e:
            st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e}")
            st.info("টিপস: গুগল এআই স্টুডিওতে আপনার কোটা শেষ হয়েছে কি না একবার চেক করুন।")

if uploaded_file:
    st.image(uploaded_file, caption="আপনার আপলোড করা ছবি", use_container_width=True)
