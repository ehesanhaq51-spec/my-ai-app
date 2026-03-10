import streamlit as st
import google.generativeai as genai

# আপনার নতুন API Key আমি এখানে বসিয়ে দিয়েছি
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"

# কনফিগারেশন
genai.configure(api_key=API_KEY)

# সব ধরণের মডেল ট্রাই করার জন্য এই সিস্টেম
def get_ai_response(prompt):
    # প্রথমে নতুন মডেল ট্রাই করবে
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except:
        # কাজ না করলে স্টেবল প্রো মডেল ট্রাই করবে
        try:
            model = genai.GenerativeModel('gemini-pro')
            return model.generate_content(prompt).text
        except Exception as e:
            return f"Error: {e}"

# ইন্টারফেস
st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")
st.write("এখন আমি অংক এবং যেকোনো প্রশ্নের উত্তর দিতে পুরোপুরি তৈরি!")

user_input = st.text_input("আপনার অংক বা প্রশ্নটি এখানে লিখুন:")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('AI উত্তর তৈরি করছে...'):
            response_text = get_ai_response(user_input)
            st.write("---")
            st.markdown(response_text)
    else:
        st.warning("আগে কিছু লিখুন ভাই!")
