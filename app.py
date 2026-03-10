import streamlit as st

st.set_page_config(page_title="Ehesan's AI", page_icon="🤖")

st.title("🤖 Ehesan's Smart AI Bot")
st.write("আপনার প্রশ্নের উত্তর দিতে আমি এখন তৈরি!")

# ইনপুট বক্স
user_input = st.text_input("এখানে কিছু লিখুন (যেমন: kemon aso):")

if user_input:
    text = user_input.lower()
    
    if "kemon aso" in text or "ki obostha" in text:
        answer = "আমি খুব ভালো আছি! আপনি কেমন আছেন?"
    elif "ki koro" in text:
        answer = "আমি আপনার সাথে কথা বলছি আর নতুন কিছু শেখার চেষ্টা করছি।"
    elif "nam ki" in text:
        answer = "আমার নাম এহসান-বট, আপনার ব্যক্তিগত সহকারী!"
    else:
        answer = "আপনার কথাটি আমি বুঝতে পেরেছি, কিন্তু আমার মাথায় এখনো সব উত্তর নেই। আমি শিখছি!"
    
    st.info(f"AI: {answer}")
