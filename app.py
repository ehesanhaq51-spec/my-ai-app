import streamlit as st
import google.generativeai as genai

# আপনার API Key এখানে বসানো আছে
API_KEY = "AIzaSyCXIudvujq26EPUcEAVmisQNNTCNFlQ-Ak"

# গুগল কনফিগারেশন - এখানে মডেলের নাম আপডেট করা হয়েছে
try:
    genai.configure(api_key=API_KEY)
    # আমরা এখানে gemini-pro ব্যবহার করছি যা সব একাউন্টে কাজ করে
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"কনফিগারেশন ভুল: {e}")

st.set_page_config(page_title="Ehesan's AI Master", page_icon="🤖")
st.title("🤖 Ehesan's Smart AI Assistant")
st.write("এখন আমি আপনার অংক এবং সব প্রশ্নের উত্তর দিতে পারব!")

user_input = st.text_input("আপনার প্রশ্নটি এখানে লিখুন:")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('গুগল উত্তর পাঠাচ্ছে...'):
            try:
                # সরাসরি উত্তর জেনারেট করা
                response = model.generate_content(user_input)
                st.write("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"গুগল থেকে উত্তর আসেনি। কারণ: {e}")
                st.info("যদি কাজ না করে, তবে গুগল এআই স্টুডিও থেকে নতুন একটি কী (Key) তৈরি করে দেখুন।")
    else:
        st.warning("আগে কিছু লিখুন ভাই!")
