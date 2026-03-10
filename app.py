import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার সচল API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# কনফিগারেশন - এখানে আমরা সরাসরি ভার্সন ফিক্স করে দিচ্ছি যাতে 404 না আসে
try:
    genai.configure(api_key=API_KEY)
    # সঠিক মডেল লোড করা
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={
            "temperature": 0.9,
            "top_p": 1,
            "max_output_tokens": 2048,
        }
    )
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
st.write("বলো বন্ধু, এখন আমি একদম তৈরি! সব ঝেড়ে কাশতে পারো। 😊")

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
                    # ছবি থাকলে ছবিসহ প্রসেস
                    response = model.generate_content([system_instruction, img, prompt])
                else:
                    # শুধু টেক্সট হলে
                    response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
                
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"ইস বন্ধু, ছোট একটা এরর হইছে: {e}")
                st.info("টিপস: গুগল এআই স্টুডিওতে আপনার কোটা শেষ হয়েছে কি না একবার চেক করুন।")
