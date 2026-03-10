import streamlit as st
import google.generativeai as genai

# আপনার API Key
API_KEY = "AIzaSyA22909TPzqXNhoogPTNHMeCDAajn2xij4"

# গুগল কনফিগারেশন এবং অটো-মডেল সিলেকশন
try:
    genai.configure(api_key=API_KEY)
    
    # আপনার কী (Key) দিয়ে কোন কোন মডেল চলে তা খুঁজে বের করা
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # অগ্রাধিকার ভিত্তিতে মডেল সেট করা
    if 'models/gemini-1.5-flash' in models:
        selected_model = 'models/gemini-1.5-flash'
    elif 'models/gemini-1.5-pro' in models:
        selected_model = 'models/gemini-1.5-pro'
    else:
        selected_model = models[0] # যেটা পাবে সেটাই নিবে
        
    model = genai.GenerativeModel(selected_model)
except Exception as e:
    st.error(f"API সংযোগে সমস্যা: {e}")

st.set_page_config(page_title="Ehesan's Pro AI", page_icon="🧠")
st.title("🧠 Ehesan's Pro AI Assistant")

# সেশন স্টেট যাতে এন্টার দিলে বক্স খালি হয়
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""

# ইনপুট বক্স
st.text_input("আপনার অংক বা প্রশ্নটি এখানে লিখুন:", key="widget", on_change=submit)

if st.session_state.user_input:
    query = st.session_state.user_input
    with st.spinner('মাস্টারমাইন AI ভাবছে...'):
        try:
            # ইনস্ট্রাকশন: ঠিক আমার মতো করে উত্তর দিতে বলা হয়েছে
            instruction = (
                "You are an expert tutor. Provide detailed, step-by-step solutions for "
                "Math, Physics, and Chemistry problems in Bengali. For general queries, "
                "be concise and helpful in Bengali. If Banglish is used, reply in Bengali."
            )
            response = model.generate_content(f"{instruction}\n\nQuestion: {query}")
            
            st.write("---")
            st.markdown(response.text)
            st.session_state.user_input = "" # বক্স ক্লিয়ার নিশ্চিত করা
        except Exception as e:
            st.error(f"দুঃখিত ভাই, আবার এরর এসেছে: {e}")
            st.info("টিপস: গুগল এআই স্টুডিওতে আপনার প্রোজেক্টে 'Gemini API' এনাবল আছে কি না নিশ্চিত করুন।")

st.button("Send 📤")
