import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"
genai.configure(api_key=API_KEY)

# মোবাইলের জন্য স্ক্রিন সেটআপ
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

# CSS দিয়ে ইন্টারফেস সুন্দর করা (মোবাইল ফ্রেন্ডলি)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextInput { position: fixed; bottom: 3rem; width: 100%; }
    .stButton { position: fixed; bottom: 3rem; right: 1rem; }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("বলো বন্ধু, আজ কী নিয়ে আড্ডা দিবা? অংক, বিজ্ঞান নাকি মনের কথা?")

# সেশন স্টেট আড্ডা মনে রাখার জন্য
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের আড্ডাগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ছবি আপলোড (ঐচ্ছিক)
uploaded_file = st.sidebar.file_uploader("ছবি পাঠাও এখানে", type=["jpg", "png", "jpeg"])

# চ্যাট ইনপুট (নিচেই থাকবে মোবাইলের মতো)
if prompt := st.chat_input("এখানে কিছু লিখুন..."):
    # ইউজারের মেসেজ দেখানো
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI এর উত্তর তৈরি
    with st.chat_message("assistant"):
        with st.spinner("বন্ধু ভাবছে..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # ফ্রেন্ডলি হওয়ার কড়া ইনস্ট্রাকশন
                system_prompt = (
                    "You are a friendly best friend of Ehesan. Speak in very casual, warm, "
                    "and joyful Bengali. Don't be too formal. If Ehesan asks about Math, "
                    "Physics, or Chemistry, explain it like a cool big brother. "
                    "Chat, joke, and be a great companion. Always use emojis! 🌟"
                )

                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_prompt, img, prompt])
                else:
                    response = model.generate_content(f"{system_prompt}\n\nUser says: {prompt}")
                
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"ইস বন্ধু, একটা ঝামেলা হইছে: {e}")
