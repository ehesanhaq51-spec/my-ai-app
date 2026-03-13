import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটআপ
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's AI Assistant", page_icon="🎬", layout="wide")

# ২. সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# ৩. সাইডবার মেনু
with st.sidebar:
    st.title("⚙️ অপশন")
    mode = st.selectbox("মোড বেছে নিন:", ["চ্যাট", "ভিডিও/অডিও স্টুডিও"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৪. চ্যাটবট
if mode == "চ্যাট":
    st.title("🤝 এহসানের বন্ধু")
    for m in st.session_state.messages:
        if m["role"] != "system":
            with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("কিছু বলো..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            r = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.3-70b-versatile")
            st.markdown(r.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant", "content": r.choices[0].message.content})

# ৫. ভিডিও ও অডিও
else:
    st.title("🎬 এআই স্টুডিও")
    text = st.text_area("অডিওর জন্য স্ক্রিপ্ট লিখুন:")
    if st.button("ভয়েস বানান"):
        if text:
            gTTS(text=text, lang='bn').save("v.mp3")
            st.audio("v.mp3")
    
    st.write("---")
    v_prompt = st.text_input("ভিডিওর জন্য ইংরেজি প্রম্পট দিন:")
    if st.button("ভিডিও জেনারেট করুন"):
        if v_prompt:
            with st.spinner("ভিডিও তৈরি হচ্ছে..."):
                try:
                    # সরাসরি টোকেন ব্যবহার করা হচ্ছে
                    output = replicate.run(
                        "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                        input={"prompt": v_prompt},
                        api_token="r8_QjBeAx7TGpUAG9FMBbAdUMftp7qpZBq1ZEv1I"
                    )
                    st.video(output)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
