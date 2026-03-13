import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি এবং ক্লায়েন্ট সেটআপ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Replicate API Key (ভিডিওর জন্য - এখানে আপনারটা বসিয়ে দিন)
# os.environ["# Replicate API Key (ভিডিওর জন্য)
os.environ["REPLICATE_API_TOKEN"] = "r8_************************************"] = "আপনার_replicate_token_এখানে"

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

# ৪. চ্যাটবট মোড (আপনার আগের কাজ)
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

# ৫. ভিডিও ও অডিও মোড (নতুন সংযোজন)
else:
    st.title("🎬 ভিডিও ও অডিও স্টুডিও")
    
    video_script = st.text_area("আপনার ভিডিওর স্ক্রিপ্ট এখানে দিন...", height=200)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 অডিও তৈরি ও ডাউনলোড"):
            if video_script:
                with st.spinner('ভয়েস তৈরি হচ্ছে...'):
                    tts = gTTS(text=video_script, lang='bn')
                    tts.save("voice.mp3")
                    st.audio("voice.mp3")
                    with open("voice.mp3", "rb") as f:
                        st.download_button("Download Audio", f, file_name="ehesan_voice.mp3")
            else:
                st.error("আগে স্ক্রিপ্ট লিখুন!")

    with col2:
        video_prompt = st.text_input("ভিডিওর দৃশ্যটি ইংরেজিতে লিখুন (যেমন: A cat playing)")
        if st.button("🎞️ জেনারেট এইচডি ভিডিও"):
            # আপনার Replicate টোকেন থাকলে এটি কাজ করবে
            if "REPLICATE_API_TOKEN" not in os.environ:
                st.warning("ভাই, সাইডবার বা কোডে আপনার Replicate API Token সেট করা নেই।")
            elif video_prompt:
                with st.spinner('১০ সেকেন্ডের হাই-কোয়ালিটি ভিডিও তৈরি হচ্ছে...'):
                    try:
                        output = replicate.run(
                            "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                            input={"prompt": video_prompt}
                        )
                        st.video(output)
                        st.success("ভিডিও রেডি! মাউসের রাইট ক্লিক করে সেভ করুন।")
                    except Exception as e:
                        st.error(f"ভিডিও তৈরিতে সমস্যা: {e}")
