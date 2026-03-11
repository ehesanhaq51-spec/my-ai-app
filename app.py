import streamlit as st
from groq import Groq

# ১. আপনার Groq API Key (এটি সঠিক আছে)
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝")
st.title("🤝 এহসানের দোস্ত AI")

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
            # আপডেট: এখানে 'llama-3.3-70b-versatile' ব্যবহার করা হয়েছে যা বর্তমানে সবচেয়ে স্টেবল
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Ehesan's best friend. Talk in very friendly Bengali. Use emojis!"},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", 
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            # এরর হলে তা পরিষ্কারভাবে দেখা যাবে
            st.error(f"ইস বন্ধু! কারিগরি সমস্যা: {str(e)}")
