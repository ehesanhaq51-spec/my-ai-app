import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার নতুন API Key (সরাসরি এখানে বসিয়ে দিলাম)
API_KEY = "AIzaSyD66p5vPPvXJo5pkoCNJIkaVqYYP7DLjSs"

# কনফিগারেশন - ভার্সন সমস্যা এড়াতে সরাসরি সেটআপ
try:
    genai.configure(api_key=API_KEY)
    # মডেল ফিক্সড করা হয়েছে যাতে 404 এরর না আসে
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config error: {e}")

# মোবাইল ফ্রেন্ডলি ডিজাইন ও ইন্টারফেস
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

# চ্যাট বক্স ও ডিজাইন সুন্দর করার জন্য CSS
st.markdown("""
    <style>
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("বলো বন্ধু, এখন আমি একদম তৈরি! সব ঝেড়ে কাশতে পারো। 😊")

# আড্ডা মনে রাখার জন্য সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের কথাগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# সাইডবারে ছবি আপলোড অপশন
with st.sidebar:
    st.header("ছবি বা ফাইল")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি দাও", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="আপলোড করা ছবি")

# চ্যাট ইনপুট (নিচেই থাকবে, সেন্ড বাটনের কাজ করবে মোবাইলের কিবোর্ড বা এন্টার)
if prompt := st.chat_input("এখানে কিছু লেখো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with
