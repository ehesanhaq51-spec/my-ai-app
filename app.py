import streamlit as st
from groq import Groq

# আপনার সঠিক API Key
client = Groq(api_key="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")

st.title("🚀 Ehesan's Final AI Assistant")

# চ্যাট বক্স
user_input = st.text_input("এখানে আপনার প্রশ্ন লিখুন:")

if st.button("Send 📤"):
    if user_input:
        try:
            # এখানে আমরা 'llama-3.3-70b-versatile' ব্যবহার করছি যা বর্তমানে সবথেকে বেশি স্টেবল
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_input}]
            )
            st.write("---")
            st.markdown(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"এরর: {e}")
    else:
        st.warning("আগে কিছু লিখুন!")
