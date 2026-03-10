import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==============================
# 🔑 API KEY
# ==============================

API_KEY = "YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Ehesan's Buddy AI",
    page_icon="🤝",
    layout="centered"
)

# ==============================
# STYLE
# ==============================

st.markdown("""
<style>

.stChatFloatingInputContainer{
bottom:20px;
}

div[data-testid="stChatMessage"]{
border-radius:15px;
padding:10px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE
# ==============================

st.title("🤝 এহসানের দোস্ত AI")
st.write("বলো বন্ধু! আমি তোমার AI দোস্ত 😎")

# ==============================
# SESSION MEMORY
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# SHOW CHAT HISTORY
# ==============================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.header("📷 ছবি আপলোড")

    uploaded_file = st.file_uploader(
        "Math / Science Problem এর ছবি দাও",
        type=["jpg","jpeg","png"]
    )

    st.divider()

    if st.button("🧹 Chat Clear"):
        st.session_state.messages=[]
        st.rerun()

# ==============================
# SYSTEM INSTRUCTION
# ==============================

system_prompt = """
You are the best friend of Ehesan.

Speak in casual friendly Bengali.
Use emojis 😊🔥😄.

Explain math and science problems
like a cool big brother.

Always reply in Bengali.
"""

# ==============================
# CHAT INPUT
# ==============================

if prompt := st.chat_input("কিছু লিখো বন্ধু..."):

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("দোস্ত ভাবছে... 🤔"):

            try:

                if uploaded_file:

                    img = Image.open(uploaded_file)

                    response = model.generate_content(
                        [system_prompt, img, prompt]
                    )

                else:

                    response = model.generate_content(
                        f"{system_prompt}\nUser:{prompt}"
                    )

                if response.text:
                    reply = response.text
                else:
                    reply = "বন্ধু ঠিক বুঝতে পারিনি 😅 আবার বলো।"

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role":"assistant","content":reply}
                )

            except Exception as e:

                st.error("একটু টেকনিক্যাল সমস্যা হয়েছে 😅")

                st.write(e)
