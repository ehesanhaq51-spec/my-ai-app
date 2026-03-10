import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"
genai.configure(api_key=API_KEY)

# মোবাইলের জন্য ডিজাইন সেটআপ
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

# CSS দিয়ে ইন্টারফেস সুন্দর ও মোবাইল ফ্রেন্ডলি করা
st.markdown("""
    <style>
    .main { background-color: #f7f9fc; }
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True) # এখানে ভুলটি ঠিক করা হয়েছে

st.title("🤝 এহসানের দোস্ত AI")
st.write("বলো বন্ধু, আজ কী নিয়ে আড্ডা দিবা? আমি এখন একদম তোমার বন্ধুর মতো!")

# সেশন স্টেট (আগের কথা মনে রাখার জন্য)
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# সাইডবারে ছবি আপলোড অপশন (যাতে স্ক্রিন পরিষ্কার থাকে)
with st.sidebar:
    st.header("ছবি পাঠান")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি দিন", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="আপলোড করা ছবি")

# চ্যাট ইনপুট (নিচেই থাকবে, এন্টার দিলেই সেন্ড হবে)
if prompt := st.chat_input("এখানে কিছু লিখুন..."):
    # ইউজারের মেসেজ স্ক্রিনে দেখানো
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI এর ফ্রেন্ডলি উত্তর তৈরি
    with st.chat_message("assistant"):
        with st.spinner("বন্ধু ভাবছে..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # ফ্রেন্ডলি ইনস্ট্রাকশন
                system_instruction = (
                    "You are the best friend of Ehesan. Always speak in a very warm, "
                    "joyful, and casual Bengali. Use emojis often! 🌟 "
                    "If Ehesan asks about Math, Physics, or Chemistry, explain it like a "
                    "cool big brother. Be funny, chatty, and supportive."
                )

                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
                
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"ইস বন্ধু, একটা সমস্যা হইছে: {e}")
