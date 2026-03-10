import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# কনফিগারেশন - সরাসরি ভার্সন ফিক্সড করে দিচ্ছি যাতে 404 না আসে
try:
    genai.configure(api_key=API_KEY)
    # আপনার চাবির আন্ডারে যে মডেলগুলো এখন কাজ করছে সেগুলো নিজে খুঁজে বের করা
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # সবচেয়ে লেটেস্টটা বেছে নেওয়া (Gemini 1.5 Flash থাকলে সেটা আগে নিবে)
    model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Config error: {e}")

# মোবাইল ফ্রেন্ডলি ডিজাইন
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("সব বাধা কাটিয়ে আমি চলে এসেছি বন্ধু! এখন প্রাণ খুলে আড্ডা দাও। 😊")

# সেশন স্টেট (আগের কথা মনে রাখার জন্য)
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# সাইডবারে ছবি আপলোড অপশন
with st.sidebar:
    st.header("ছবি বা ফাইল")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞান সমস্যার ছবি দাও", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="আপলোড করা ছবি")

# চ্যাট ইনপুট
if prompt := st.chat_input("এখানে তোমার প্রশ্ন বা মনের কথা লেখো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI এর উত্তর
    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # ফ্রেন্ডলি হওয়ার চূড়ান্ত ইনস্ট্রাকশন
                system_instruction = (
                    "You are the best friend of Ehesan. Always speak in a very warm, "
                    "joyful, and casual Bengali. Use emojis like 😊, 🌟, 🔥 often! "
                    "If Ehesan asks about Math, Physics, or Chemistry, explain it like a "
                    "cool elder brother. Be funny, chatty, and supportive. "
                    "Answer strictly in Bengali."
                )

                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    response
