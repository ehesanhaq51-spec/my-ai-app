import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটআপ
GROQ_API_KEY = "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"
REPLICATE_TOKEN = "r8_EsCZJpWO67kYD5KnljjSRfuWKKWUvc544ls03"

client = Groq(api_key=GROQ_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

st.set_page_config(page_title="Ehesan's AI Studio", page_icon="🎬", layout="wide")

# ২. সাইডবার মেনু
with st.sidebar:
    st.title("⚙️ মেনু")
    mode = st.selectbox("কি করতে চান?", ["চ্যাটবট", "ভিডিও ও অডিও মেকার"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৩. চ্যাট মোড
if mode == "চ্যাটবট":
    st.title("🤝 এহসানের বন্ধু")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a friendly assistant."}]
    
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

# ৪. ভিডিও ও অডিও মোড
else:
    st.title("🎬 ভিডিও ও অডিও স্টুডিও")
    
    script = st.text_area("অডিওর জন্য বাংলা স্ক্রিপ্ট:")
    if st.button("ভয়েস বানান"):
        if script:
            gTTS(text=script, lang='bn').save("v.mp3")
            st.audio("v.mp3")
    
    st.write("---")
    
    v_prompt = st.text_input("ভিডিওর জন্য ইংরেজি বর্ণনা (যেমন: A cat playing):")
    if st.button("ভিডিও জেনারেট করুন"):
        if v_prompt:
            with st.spinner("ভিডিও তৈরি হচ্ছে..."):
                try:
                    # সরাসরি টোকেন দিয়ে রান করা হচ্ছে
                    output = replicate.run(
                        "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                        input={"prompt": v_prompt},
                        api_token=REPLICATE_TOKEN
                    )
                    st.video(output)
                except Exception as e:
                    st.error(f"এরর: {str(e)}")
