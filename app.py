import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার API Key
API_KEY = "AIzaSyCkIZAsWEqoJU88GyKR61m-vxrJ3R_3dnQ"

# কনফিগারেশন - এখানে আমরা সরাসরি API Version ফিক্সড করে দিচ্ছি
try:
    # সরাসরি 'v1' ভার্সন ব্যবহার করে কনফিগার করা
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
    model_name = "gemini-1.5-flash"
except Exception as e:
    st.error(f"Config error: {e}")

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝", layout="centered")

st.markdown("""
    <style>
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 এহসানের দোস্ত AI")
st.write("সব বাধা কাটিয়ে আমি চলে এসেছি বন্ধু! 😊")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.header("ছবি পাঠান")
    uploaded_file = st.file_uploader("অংক বা বিজ্ঞানের ছবি দাও", type=["jpg", "png", "jpeg"])

if prompt := st.chat_input("এখানে কিছু লেখো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                system_instruction = (
                    "You are the best friend of Ehesan. Speak in very casual and joyful Bengali. "
                    "Use emojis! 😊 Solve math/science problems like a cool big brother. "
                    "Always reply in Bengali."
                )
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[system_instruction, img, prompt]
                    )
                else:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"{system_instruction}\n\nUser: {prompt}"
                    )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"এখনো সমস্যা হচ্ছে বন্ধু: {e}")
