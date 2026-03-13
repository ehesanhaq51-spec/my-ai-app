import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটআপ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's AI Studio", page_icon="🎬", layout="wide")

# ২. সেশন স্টেট (চ্যাট মনে রাখার জন্য)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a friendly assistant for Ehesan."}]

# ৩. সাইডবার মেনু
with st.sidebar:
    st.title("⚙️ মেনু")
    mode = st.selectbox("মোড বেছে নিন:", ["চ্যাট", "ভিডিও ও অডিও স্টুডিও"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৪. চ্যাটবট অংশ
if mode == "চ্যাট":
    st.title("🤝 এহসানের বন্ধু")
    for m in st.session_state.messages:
        if m["role"] != "system":
            with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("কিছু বলো বন্ধু..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            r = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.3-70b-versatile")
            st.markdown(r.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant", "content": r.choices[0].message.content})

# ৫. ভিডিও ও অডিও স্টুডিও অংশ
else:
    st.title("🎬 এআই ভিডিও ও অডিও মেকার")
    
    st.subheader("🔊 ১. বাংলা ভয়েস তৈরি")
    text = st.text_area("অডিওর জন্য বাংলা স্ক্রিপ্ট লিখুন (যেমন: আসসালামু আলাইকুম বন্ধুরা...):")
    if st.button("ভয়েস জেনারেট করুন"):
        if text:
            with st.spinner("ভয়েস তৈরি হচ্ছে..."):
                gTTS(text=text, lang='bn').save("v.mp3")
                st.audio("v.mp3")
                st.success("ভয়েস রেডি! নিচের ডাউনলোড বাটনে ক্লিক করুন।")
    
    st.write("---")
    
    st.subheader("🎞️ ২. এআই ভিডিও তৈরি")
    v_prompt = st.text_input("ভিডিওর দৃশ্যটি ইংরেজিতে লিখুন:", placeholder="Ex: A cat playing in a garden, cinematic 4k")
    if st.button("এইচডি ভিডিও তৈরি করুন"):
        if v_prompt:
            with st.spinner("ভিডিও তৈরি হতে ১-২ মিনিট সময় নিতে পারে। একটু ধৈর্য ধরুন..."):
                try:
                    # আপনার নতুন টোকেনটি এখানে সরাসরি দেওয়া হয়েছে
                    output = replicate.run(
                        "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                        input={"prompt": v_prompt},
                        api_token="r8_EsCZJpWO67kYD5KnljjSRfuWKKWUvc544ls03"
                    )
                    st.video(output)
                    st.success("অভিনন্দন! আপনার ভিডিও তৈরি হয়ে গেছে।")
                except Exception as e:
                    st.error(f"দুঃখিত বন্ধু, একটি সমস্যা হয়েছে: {str(e)}")
        else:
            st.warning("ভিডিওর জন্য আগে একটি ইংরেজি বর্ণনা (Prompt) লিখুন।")
