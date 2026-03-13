import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি এবং ক্লায়েন্ট সেটআপ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Replicate API Key (আপনার দেওয়া টোকেনটি এখানে বসিয়ে দিলাম)
os.environ["REPLICATE_API_TOKEN"] = "r8_QjBeAx7TGpUAG9FMBbAdUMftp7qpZBq1ZEv1I"

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🎬", layout="wide")

# ২. চ্যাট স্মৃতিশক্তি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali and remember what was discussed before."}
    ]

# ৩. সাইডবার ডিজাইন
with st.sidebar:
    st.title("⚙️ কনফিগারেশন")
    app_mode = st.selectbox("কি করতে চান?", ["এহসানের বন্ধু (Chat)", "ভিডিও ও অডিও মেকার"])
    
    if st.button("চ্যাট ক্লিয়ার করো"):
        st.session_state.messages = [
            {"role": "system", "content": "You are Ehesan's best friend. Always speak in friendly Bengali."}
        ]
        st.rerun()
    
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৪. চ্যাটবট মোড
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
                response = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"ইস বন্ধু! কারিগরি সমস্যা: {str(e)}")

# ৫. ভিডিও ও অডিও মোড
else:
    st.title("🎬 ভিডিও ও অডিও স্টুডিও")
    
    video_script = st.text_area("আপনার ভিডিওর স্ক্রিপ্ট এখানে দিন (ভয়েস ওভারের জন্য)...", height=150)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔊 অডিও জেনারেটর")
        if st.button("অডিও তৈরি করুন"):
            if video_script:
                with st.spinner('ভয়েস তৈরি হচ্ছে...'):
                    try:
                        tts = gTTS(text=video_script, lang='bn')
                        tts.save("voice.mp3")
                        st.audio("voice.mp3")
                        with open("voice.mp3", "rb") as f:
                            st.download_button("ডাউনলোড অডিও", f, file_name="ehesan_voice.mp3")
                    except Exception as e:
                        st.error(f"অডিও তৈরিতে সমস্যা: {e}")
            else:
                st.warning("আগে উপরের বক্সে কিছু লিখুন!")

    with col2:
        st.subheader("🎞️ ভিডিও জেনারেটর")
        video_prompt = st.text_input("ভিডিওর দৃশ্যটি ইংরেজিতে লিখুন...", placeholder="Ex: A tiger in a forest, cinematic 4k")
        if st.button("এইচডি ভিডিও তৈরি করুন"):
            if video_prompt:
                with st.spinner('১০ সেকেন্ডের হাই-কোয়ালিটি ভিডিও তৈরি হচ্ছে (১-২ মিনিট সময় লাগতে পারে)...'):
                    try:
                        # Luma Dream Machine মডেল ব্যবহার করা হচ্ছে
                        output = replicate.run(
                            "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                            input={"prompt": video_prompt}
                        )
                        st.video(output)
                        st.success("ভিডিও তৈরি হয়েছে! মাউসের রাইট ক্লিক করে সেভ করুন।")
                    except Exception as e:
                        st.error(f"ভিডিও তৈরিতে সমস্যা: {e}")
            else:
                st.warning("ভিডিওর জন্য একটি
