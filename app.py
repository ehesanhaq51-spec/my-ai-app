import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. আপনার নতুন API Key
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# ২. কনফিগারেশন - সরাসরি 'rest' ব্যবহার করে ৪-০-৪ এরর সমাধান করা হয়েছে
try:
    genai.configure(api_key=API_KEY, transport='rest')
    # gemini-1.5-flash মডেলটিই সবচেয়ে ভালো এবং দ্রুত কাজ করবে
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"কনফিগারেশনে সমস্যা: {e}")

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

# ৪. আড্ডা মনে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. সাইডবারে ফাইল আপলোড
with st.sidebar:
    st.header("ছবি বা ফাইল")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি দাও", type=["jpg", "png", "jpeg"])

# ৬. চ্যাট ইনপুট ও উত্তর জেনারেট করা
if prompt := st.chat_input("এখানে কিছু লেখো বন্ধু..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # ফ্রেন্ডলি ইনস্ট্রাকশন
                system_instruction = (
                    "You are the best friend of Ehesan. Speak in very casual and joyful Bengali. "
                    "Use lots of emojis! 😊 Solve math/science problems easily. "
                    "Always reply in Bengali."
                )
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    response = model.generate_content(f"{system_instruction}\n\nUser Question: {prompt}")
                
                ai_reply = response.text
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                # এররটি সহজভাবে দেখানো
                st.error("ইস বন্ধু, ছোট একটা কারিগরি সমস্যা হয়েছে।")
                st.info(f"এরর ডিটেইলস: {e}")
