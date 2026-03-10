import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. আপনার নতুন API Key
API_KEY = "AIzaSyD66p5vPPvXJo5pkoCNJIkaVqYYP7DLjSs"

# ২. সরাসরি কনফিগারেশন - ভার্সন সমস্যা এড়াতে
try:
    genai.configure(api_key=API_KEY)
    # সঠিক মডেল সরাসরি ডিফাইন করা হয়েছে
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"কনফিগারেশনে সমস্যা হয়েছে: {e}")

# ৩. ইন্টারফেস ডিজাইন (মোবাইল ফ্রেন্ডলি)
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("বলো বন্ধু, এখন আমি একদম তৈরি! সব ঝেড়ে কাশতে পারো। 😊")

# ৪. আড্ডা মনে রাখার সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. সাইডবারে ফাইল আপলোড (অংক বা বিজ্ঞানের ছবির জন্য)
with st.sidebar:
    st.header("ছবি বা ফাইল")
    uploaded_file = st.file_uploader("সমস্যার ছবি দাও", type=["jpg", "png", "jpeg"])

# ৬. চ্যাট ইনপুট ও উত্তর জেনারেট করা
if prompt := st.chat_input("এখানে কিছু লেখো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # ফ্রেন্ডলি ইনস্ট্রাকশন
                system_instruction = (
                    "You are the best friend of Ehesan. Speak in very casual and joyful Bengali. "
                    "Use lots of emojis like 😊, 🌟, 🔥! Solve math/science problems like a cool big brother. "
                    "Always reply in Bengali."
                )
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
                
                ai_reply = response.text
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                # এরর মেসেজ সহজ বাংলায়
                st.error("ইস বন্ধু, ছোট একটা কারিগরি সমস্যা হয়েছে। গুগল এআই স্টুডিওতে আপনার লিমিট শেষ কি না দেখুন।")
                st.info(f"টেকনিক্যাল ডিটেইলস: {e}")
