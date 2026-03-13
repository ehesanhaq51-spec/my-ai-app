import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটআপ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's AI Studio", page_icon="🎬", layout="wide")

# ২. চ্যাট মেমোরি
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a friendly assistant for Ehesan."}]

# ৩. সাইডবার মেনু
with st.sidebar:
    st.title("⚙️ সেটিংস")
    mode = st.selectbox("কি করতে চান?", ["চ্যাটবট", "ভিডিও ও অডিও মেকার"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৪. চ্যাটবট মোড
if mode == "চ্যাটবট":
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

# ৫. ভিডিও ও অডিও মোড
else:
    st.title("🎬 এআই ভিডিও ও অডিও স্টুডিও")
    
    # অডিও পার্ট
    script = st.text_area("অডিওর জন্য বাংলা স্ক্রিপ্ট লিখুন:")
    if st.button("ভয়েস বানান"):
        if script:
            gTTS(text=script, lang='bn').save("v.mp3")
            st.audio("v.mp3")
    
    st.write("---")
    
    # ভিডিও পার্ট
    v_prompt = st.text_input("ভিডিওর জন্য ইংরেজি প্রম্পট দিন (যেমন: A cat playing):")
    if st.button("ভিডিও জেনারেট করুন"):
        if v_prompt:
            with st.spinner("আপনার এআই ভিডিও তৈরি হচ্ছে... ১-২ মিনিট ধৈর্য ধরুন।"):
                try:
                    # আপনার নতুন টোকেনটি এখানে সরাসরি বসিয়ে দিলাম
                    output = replicate.run(
                        "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                        input={"prompt": v_prompt},
                        api_token="r8_EsCZJpWO67kYD5KnljjSRfuWKKWUvc544ls03"
                    )
                    st.video(output)
                    st.success("অভিনন্দন! ভিডিও তৈরি হয়ে গেছে।")
                except Exception as e:
                    st.error(f"এরর: {str(e)}")
