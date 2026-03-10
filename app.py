import streamlit as st
from groq import Groq

# আপনার Groq API Key এখানে বসান
GROQ_API_KEY = "আপনার_Groq_API_Key_এখানে_দিন"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's Llama Buddy", page_icon="🦙")
st.title("🦙 এহসানের নতুন দোস্ত (Llama)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Meta-র সবথেকে শক্তিশালী ওপেন সোর্স মডেল Llama 3 ব্যবহার করা হয়েছে
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Ehesan's best friend. Speak in joyful Bengali."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192", # এটি খুব দ্রুত কাজ করে
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"ইস! ছোট একটা সমস্যা: {e}")
