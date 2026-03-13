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

# ২. সাইডবার
with st.sidebar:
    st.title("⚙️ মেনু")
    mode = st.selectbox("কি করতে চান?", ["চ্যাটবট", "ভিডিও ও অডিও মেকার"])
    st.write("---")
    st.info("ডেভেলপার: এহসান")

# ৩. ভিডিও ও অডিও মোড
if mode == "ভিডিও ও অডিও মেকার":
    st.title("🎬 এআই ভিডিও ও অডিও স্টুডিও")
    
    script = st.text_area("অডিওর জন্য বাংলা স্ক্রিপ্ট:")
    if st.button("ভয়েস বানান"):
        if script:
            gTTS(text=script, lang='bn').save("v.mp3")
            st.audio("v.mp3")
    
    st.write("---")
    
    v_prompt = st.text_input("ভিডিওর জন্য ইংরেজি বর্ণনা (যেমন: A cute cat playing in garden):")
    if st.button("ভিডিও জেনারেট করুন"):
        if v_prompt:
            with st.spinner("ম্যাজিক শুরু হচ্ছে... ১ মিনিট অপেক্ষা করুন।"):
                try:
                    # এখানে সরাসরি লুমা ড্রিম মেশিন ব্যবহার হচ্ছে
                    output = replicate.run(
                        "lucataco/luma-dream-machine:13677273-030b-40b9-9a25-e51c9113e790",
                        input={"prompt": v_prompt}
                    )
                    st.video(output)
                    st.success("অভিনন্দন! ভিডিও তৈরি হয়েছে।")
                except Exception as e:
                    if "401" in str(e):
                        st.error("ভাই, আপনার Replicate টোকেনটা কাজ করছে না। দয়া করে Replicate ড্যাশবোর্ডে গিয়ে দেখুন আপনার ইমেইল ভেরিফাই করা কি না বা ফ্রি ক্রেডিট আছে কি না।")
                    else:
                        st.error(f"এরর: {str(e)}")
else:
    st.title("🤝 এহসানের চ্যাট বন্ধু")
    st.write("এখানে আপনি এআই এর সাথে চ্যাট করতে পারবেন।")
