import streamlit as st
import google.generativeai as genai
from PIL import Image

# আপনার Gemini API Key
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"
genai.configure(api_key=API_KEY)

# পেজ কনফিগারেশন
st.set_page_config(page_title="Ehesan's Pro AI Master", page_icon="🧠")
st.title("🧠 Ehesan's Visionary AI")
st.write("আমি এখন ছবি দেখে আপনার অংক, পদার্থবিজ্ঞান ও রসায়নের সমাধান দিতে পারি!")

# চ্যাট হিস্ট্রি বক্স খালি করার ট্রিক
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def submit():
    st.session_state.input_text = st.session_state.widget
    st.session_state.widget = ""

# ছবি আপলোড করার অপশন (অংক বা নোটের ছবি দেওয়ার জন্য)
uploaded_file = st.file_uploader("অংক বা সমস্যার ছবি আপলোড করুন", type=["jpg", "jpeg", "png"])

# টেক্সট ইনপুট
user_query = st.text_input("আপনার প্রশ্ন লিখুন:", key="widget", on_change=submit)
final_query = st.session_state.input_text

if st.button("Send 📤") or final_query:
    query_to_use = final_query if final_query else "এই ছবিতে কী আছে বুঝিয়ে বলো।"
    
    with st.spinner('বিশ্লেষণ করছি...'):
        try:
            # এখানে 'gemini-1.5-flash' ব্যবহার করছি যা ছবি ও বাংলা দুটোই সেরা বোঝে
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                # ছবি এবং টেক্সট একসাথে প্রসেস করা
                response = model.generate_content([
                    "You are an expert teacher. Explain the problem in the image clearly in Bengali. Solve any math, physics, or chemistry problem step by step.", 
                    img, 
                    query_to_use
                ])
            else:
                # শুধু টেক্সট হলে
                response = model.generate_content(f"সবসময় বাংলায় উত্তর দাও। প্রশ্ন: {query_to_use}")
            
            st.write("---")
            st.markdown(response.text)
            st.session_state.input_text = "" # উত্তর দেখানোর পর প্রশ্ন মুছে ফেলা
            
        except Exception as e:
            st.error(f"দুঃখিত ভাই, একটি সমস্যা হয়েছে: {e}")

if uploaded_file:
    st.image(uploaded_file, caption="আপনার আপলোড করা ছবি", use_container_width=True)
