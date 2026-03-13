import streamlit as st
from groq import Groq
from gtts import gTTS
import replicate
import os

# ১. এপিআই কি সেটিংস
GROQ_API_KEY = "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"
REPLICATE_TOKEN = "r8_EsCZJpWO67kYD5KnljjSRfuWKKWUvc544ls03"

client = Groq(api_key=GROQ_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

st.set_page_config(page_title="Ehesan's AI Master", page_icon="🎬", layout="wide")

# ২. চ্যাটবট অংশ (এটি সব সময় কাজ করবে)
with st.sidebar:
    st.title("⚙️ অপশন")
    mode = st.selectbox("বেছে নিন:", ["চ্যাট বন্ধু", "ভিডিও ও অডিও স্টুডিও"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

if mode == "চ্যাট বন্ধু":
    st.title("🤝 এহসানের এআই বন্ধু")
    st.info("ভিডিও টোকেন কাজ না করলেও আপনি এখানে চ্যাট করতে পারবেন।")
    if p := st.chat_input("কিছু জিজ্ঞাসা করো..."):
        with st.chat_message("user"): st.write(p)
        r = client.chat.completions.create(messages=[{"role": "user", "content": p}], model="llama-3.3-70b-versatile")
        with st.chat_message("assistant"): st.write(r.choices[0].message.content)

# ৩. ভিডিও ও অডিও স্টুডিও
else:
    st.title("🎬 এআই ভিডিও ও অডিও মেকার")
    
    # অডিও অংশ (১০০% কাজ করবে)
    script = st.text_area("অডিওর জন্য বাংলা লিখুন:")
    if st.button("ভয়েস তৈরি করুন"):
        if script:
            gTTS(text=script, lang='bn').save("v.mp3")
            st.audio("v.mp3")
            st.success("ভয়েস তৈরি হয়েছে!")

    st.write("---")
    
    # ভিডিও অংশ
    st.subheader("🎞️ ভিডিও জেনারেটর")
    st.warning("যদি Replicate টোকেন এরর দেয়, তবে [replicate.com](https://replicate.com) এ গিয়ে আপনার একাউন্ট স্ট্যাটাস চেক করুন।")
    v_prompt = st.text_input("ভিডিওর দৃশ্য (English):")
    if st.button("ভিডিও জেনারেট"):
        if v_prompt:
            try:
                output = replicate.run(
                    "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                    input={"prompt": v_prompt}
                )
                st.video(output)
            except Exception as e:
                st.error("টোকেন সমস্যা! বিকল্প হিসেবে আপনি RunwayML বা Pika.art ব্যবহার করতে পারেন।")
