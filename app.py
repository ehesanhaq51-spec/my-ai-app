import streamlit as st

st.title("Ehesan's AI Bot")
st.write("Hello! I am your AI assistant.")

input_text = st.text_input("Ask me anything:")
if input_text:
    st.write(f"You said: {input_text}")
