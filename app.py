import streamlit as st
from groq import Groq

# ১. আপনার Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝")
st.title("Ehesan AI Assistant ")

# ২. চ্যাট হিস্ট্রি বা স্মৃতিশক্তি সেটআপ
if "messages" not in st.session_state:
    # শুরুতে একটি সিস্টেম মেসেজ দিয়ে দিচ্ছি যাতে সে তার চরিত্র মনে রাখে
    st.session_state.messages = [
        {"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali and remember what was discussed before."}
    ]

# ৩. আগের সব মেসেজ স্ক্রিনে দেখানো
for msg in st.session_state.messages:
    if msg["role"] != "system": # সিস্টেম মেসেজ দেখানোর দরকার নেই
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ৪. নতুন চ্যাট ইনপুট
if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
    # ইউজারের কথা স্মৃতিতে রাখা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # এখানে পুরো st.session_state.messages পাঠানো হচ্ছে, তাই সে আগের কথা মনে রাখবে
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            # এআই-এর কথা স্মৃতিতে রাখা
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"ইস বন্ধু! কারিগরি সমস্যা: {str(e)}")
            # সাইডবারে একটি বাটন যোগ করা (এটি app.py এর একদম শেষে দিতে পারেন)
with st.sidebar:
    st.title("কনফিগারেশন")
    if st.button("চ্যাট ক্লিয়ার করো"):
        st.session_state.messages = [
            {"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali."}
        ]
        st.rerun()
    
    st.write("---")
    st.write("ডেভেলপার: এহসান")
