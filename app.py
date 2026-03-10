import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. আপনার সঠিক API Key
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# ২. ম্যাজিক লাইন (এটি v1beta এররটি চিরতরে বন্ধ করবে)
# transport='rest' ব্যবহার করলে এটি সরাসরি স্টেবল ভার্সন ব্যবহার করে
genai.configure(api_key=API_KEY, transport='rest')

# ৩. মডেল সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash')

# বাকি কোড আপনার আগের মতোই সহজভাবে রাখা হয়েছে
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝")
st.title("🤝 এহসানের দোস্ত AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    uploaded_file = st.file_uploader("ছবি দাও (Math/Science)", type=["jpg", "png", "jpeg"])

if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ভাবছি..."):
            try:
                # সিস্টেম প্রম্পট যাতে সে আপনার বন্ধুর মতো কথা বলে
                sys_msg = "তুমি এহসানের বেস্ট ফ্রেন্ড। বাংলায় মজার কথা বলো।"
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([sys_msg, img, prompt])
                else:
                    response = model.generate_content(f"{sys_msg}\nUser: {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"ইস! আবার এরর: {e}")
