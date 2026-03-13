import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# ১. গ্রক এপিআই কি (আপনার চ্যাটবটের জন্য এটি দরকার)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's Smart AI", page_icon="🚀", layout="wide")

# ২. চ্যাটবট ও স্টুডিও মেনু
with st.sidebar:
    st.title("🌟 কন্ট্রোল প্যানেল")
    app_mode = st.selectbox("বেছে নিন:", ["চ্যাট বন্ধু", "অডিও ও ভিডিও গাইড"])
    st.write("---")
    st.write("ডেভেলপার: এহসান")

# ৩. চ্যাটবট মোড (এটি ১০০% কাজ করবে)
if app_mode == "চ্যাট বন্ধু":
    st.title("🤝 এহসানের ডিজিটাল বন্ধু")
    st.info("টোকেন ঝামেলা ছাড়াই এখানে প্রাণ খুলে কথা বলুন।")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("বন্ধু, কেমন আছো?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ৪. অডিও ও ভিডিও গাইড মোড
else:
    st.title("🎬 স্টুডিও গাইড")
    
    # অডিও অংশ
    st.subheader("🔊 ১. বাংলা ভয়েস জেনারেটর")
    audio_text = st.text_area("বাংলায় কিছু লিখুন:")
    if st.button("ভয়েস তৈরি করুন"):
        if audio_text:
            tts = gTTS(text=audio_text, lang='bn')
            tts.save("voice.mp3")
            st.audio("voice.mp3")
            st.success("ভয়েস তৈরি হয়েছে!")

    st.write("---")
    
    # ভিডিও অংশ (সরাসরি ফ্রি এআই লিঙ্ক)
    st.subheader("🎞️ ২. ফ্রি ভিডিও জেনারেটর")
    st.markdown("""
    ভাই, Replicate-এ টোকেন ঝামেলা এড়াতে আপনি নিচের এই **ফ্রি এআই টুলগুলো** সরাসরি ব্যবহার করতে পারেন। আপনার প্রম্পটটি নিচের লিঙ্কে গিয়ে লিখলেই চমৎকার ভিডিও পাবেন:
    
    * **[RunwayML](https://runwayml.com/)** - প্রফেশনাল ভিডিওর জন্য সেরা।
    * **[Luma Dream Machine](https://lumalabs.ai/dream-machine)** - আপনার কোডে যে মডেলটি ছিল, সেটি এখানে একদম ফ্রিতে ব্যবহার করা যায়।
    * **[Pika Art](https://pika.art/)** - এনিমেশন তৈরির জন্য দারুণ।
    """)
    st.info("আপনার স্ক্রিপ্টটি ইংরেজিতে অনুবাদ করতে চাইলে বাম পাশের 'চ্যাট বন্ধু' ব্যবহার করুন।")
