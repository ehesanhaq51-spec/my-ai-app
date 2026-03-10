import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. আপনার সঠিক API Key
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# ২. সার্ভার ফিক্স: transport='rest' ব্যবহার করলে ৪-০-৪ এরর চিরতরে বন্ধ হবে
try:
    genai.configure(api_key=API_KEY, transport='rest')
    # এখানে 'client' এর বদলে সরাসরি 'model' ব্যবহার করা হয়েছে
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"কনফিগারেশন এরর: {e}")

# ৩. ইন্টারফেস ডিজাইন
st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

st.title("🤝 AI")
st.write("বলো বন্ধু, এখন আমি একদম তৈরি! সব ঝেড়ে কাশতে পারো। 😊")

# ৪. আড্ডা মনে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ৫. সাইডবারে ফাইল আপলোড
with st.sidebar:
    st.header("ছবি বা ফাইল")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞানের ছবি দাও", type=["jpg", "png", "jpeg"])

# ৬. চ্যাট ও উত্তর জেনারেট করা
if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # আপনার বন্ধুর মতো পারসোনালিটি
                sys_prompt = "তুমি এহসানের বেস্ট ফ্রেন্ড। বাংলায় খুব মজার কথা বলো। অংক বা বিজ্ঞান সহজে বুঝিয়ে দাও।"
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([sys_prompt, img, prompt])
                else:
                    response = model.generate_content(f"{sys_prompt}\n\nUser: {prompt}")
                
                full_reply = response.text
                st.markdown(full_reply)
                st.session_state.messages.append({"role": "assistant", "content": full_reply})
            except Exception as e:
                # এরর হলে তা সহজভাবে দেখানো
                st.error("ইস বন্ধু! ছোট একটা কারিগরি সমস্যা হয়েছে।")
                st.info(f"প্রযুক্তিগত এরর: {e}")
