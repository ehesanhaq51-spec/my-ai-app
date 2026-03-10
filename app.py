import streamlit as st
import google.generativeai as genai

# --- কনফিগারেশন (আপনার দেওয়া কি এখানে বসানো হয়েছে) ---
API_KEY = "AIzaSyCXIudvujq26EPUcEAVmisQNNTCNFlQ-Ak"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key সেট করতে সমস্যা হয়েছে!")

# --- ইন্টারফেস সেটআপ ---
st.set_page_config(page_title="Ehesan's AI Master", page_icon="🤖")
st.title("🤖 Ehesan's Smart AI Assistant")
st.write("যেকোনো অংক বা সাধারণ প্রশ্ন লিখুন, আমি উত্তর দিচ্ছি!")

# ইউজার ইনপুট এবং সেন্ড বাটন
user_input = st.text_input("আপনার প্রশ্নটি এখানে লিখুন:", placeholder="যেমন: ৫১৫ / ৫ = কত?")
send_button = st.button("Send 📤")

if send_button:
    if user_input:
        with st.spinner('AI ভাবছে...'):
            try:
                # সরাসরি গুগল জেমিনি থেকে উত্তর আনা হচ্ছে
                response = model.generate_content(user_input)
                st.write("---")
                st.markdown(f"**AI উত্তর:**\n\n{response.text}")
            except Exception as e:
                st.error("দুঃখিত, গুগল থেকে উত্তর আনতে সমস্যা হচ্ছে। কী-টি সচল কি না চেক করুন।")
    else:
        st.warning("আগে কিছু লিখুন ভাই!")
