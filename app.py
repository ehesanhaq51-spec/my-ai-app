import streamlit as st
import google.generativeai as genai
from PIL import Image

# =========================
# API KEY (আপনার নতুন কী)
# =========================
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# transport='rest' যোগ করা হয়েছে যাতে 404 এরর না আসে
genai.configure(api_key=API_KEY, transport='rest')

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# PAGE
# =========================
st.set_page_config(
    page_title="Ehesan Buddy AI",
    page_icon="🤝"
)

st.title("🤝 এহসানের দোস্ত AI")

# =========================
# MEMORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    uploaded_file = st.file_uploader(
        "ছবি দাও (Math / Science)",
        type=["png","jpg","jpeg"]
    )

# =========================
# SYSTEM PROMPT
# =========================
system_prompt = """
তুমি এহসানের ভালো বন্ধু।
সবসময় মজার বাংলায় উত্তর দাও 😊
Math বা science সহজভাবে বুঝাও।
Always answer in Bengali.
"""

# =========================
# CHAT
# =========================
if prompt := st.chat_input("কিছু লিখো বন্ধু..."):

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ভাবছি... 🤔"):
            try:
                # সিস্টেম প্রম্পটটি সহ ইনপুট পাঠানো
                full_content = f"{system_prompt}\n\nUser Question: {prompt}"

                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    response = model.generate_content(
                        [full_content, image]
                    )
                else:
                    response = model.generate_content(full_content)

                reply = response.text
                st.markdown(reply)

                st.session_state.messages.append(
                    {"role":"assistant","content":reply}
                )

            except Exception as e:
                # আপনার স্ক্রিনশটের মতো এরর হ্যান্ডেল করা
                st.error("ইস বন্ধু, একটা কারিগরি সমস্যা হয়েছে!")
                st.write(f"Technical details: {e}")
