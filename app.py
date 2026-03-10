import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# কনফিগারেশন - সরাসরি মডেল ডিফাইন করে এরর কমানো হয়েছে
try:
    genai.configure(api_key=API_KEY)
    # সঠিক মডেল লোড করা
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config error: {e}")

# মোবাইল ফ্রেন্ডলি ইন্টারফেস ডিজাইন
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

# CSS দিয়ে চ্যাট বক্স সুন্দর করা
st.markdown("""
    <style>
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("সব বাধা কাটিয়ে আমি চলে এসেছি বন্ধু! এখন প্রাণ খুলে আড্ডা দাও। 😊")

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

# চ্যাট ইনপুট (নিচেই থাকবে, এন্টার দিলেই সেন্ড হবে)
if prompt := st.chat_input("এখানে কিছু লেখো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # ফ্রেন্ডলি হওয়ার কড়া ইনস্ট্রাকশন
                system_instruction = (
                    "You are the best friend of Ehesan. Speak in very casual and joyful Bengali. "
                    "Use lots of emojis! 😊 Solve math/science problems like a cool big brother. "
                    "Be funny and very supportive. Always reply in Bengali."
                )
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # এরর মেসেজ সহজ বাংলায় দেখানো
                st.error(f"ইস বন্ধু, ছোট একটা ঝামেলা হইছে। আমার 'মগজ' (API) হয়তো এখনো কানেক্ট হতে পারেনি। একটু পরে আবার চেষ্টা করো।")
                st.info(f"প্রযুক্তিগত এরর: {e}")
