import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটআপ (আমি আপনার টোকেনগুলো এখানে বসিয়ে দিয়েছি)
GROQ_API_KEY = "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"
REPLICATE_TOKEN = "r8_QjBeAx7TGpUAG9FMBbAdUMftp7qpZBq1ZEv1I"

client = Groq(api_key=GROQ_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🎬", layout="wide")

# ২. স্মৃতিশক্তি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali."}
    ]

# ৩. সাইডবার
with st.sidebar:
    st.title("⚙️ মেনু")
    app_mode = st.selectbox("কি করতে চান?", ["এহসানের বন্ধু (Chat)", "ভিডিও ও অডিও মেকার"])
    if st.button("চ্যাট ক্লিয়ার করো"):
        st.session_state.messages = [{"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali."}]
        st.rerun()
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৪. চ্যাট মোড
if app_mode == "এহসানের বন্ধু (Chat)":
    st.title("🤝 Ehesan AI Assistant")
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.3-70b-versatile")
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"ইস বন্ধু! সমস্যা হয়েছে: {str(e)}")

# ৫. ভিডিও ও অডিও মোড
else:
    st.title("🎬 ভিডিও ও অডিও স্টুডিও")
    video_script = st.text_area("অডিওর জন্য বাংলা স্ক্রিপ্ট লিখুন...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔊 অডিও")
        if st.button("ভয়েস তৈরি করুন"):
            if video_script:
                with st.spinner('তৈরি হচ্ছে...'):
                    tts = gTTS(text=video_script, lang='bn')
                    tts.save("voice.mp3")
                    st.audio("voice.mp3")
            else:
                st.warning("আগে কিছু লিখুন!")

    with col2:
        st.subheader("🎞️ ভিডিও")
        video_prompt = st.text_input("ভিডিওর দৃশ্যটি ইংরেজিতে লিখুন (যেমন: A cat playing)")
        if st.button("ভিডিও জেনারেট করুন"):
            if video_prompt:
                with st.spinner('ভিডিও তৈরি হচ্ছে... একটু সময় লাগবে।'):
                    try:
                        output = replicate.run(
                            "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                            input={"prompt": video_prompt}
                        )
                        st.video(output)
                    except Exception as e:
                        st.error(f"ভিডিও এরর: {e}")
            else:
                st.warning("ভিডিওর জন্য ইংরেজি প্রম্পট দিন!")
