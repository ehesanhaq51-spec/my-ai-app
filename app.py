import streamlit as st
import requests
import json

# ১. আপনার এপিআই কী (এটি সঠিক আছে)
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# ২. সরাসরি এপিআই ইউআরএল (৪-০-৪ এরর এড়াতে এটি সেরা উপায়)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝")
st.title("🤝 এহসানের দোস্ত AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট হিস্ট্রি দেখানো
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# চ্যাট ইনপুট
if prompt := st.chat_input("কিছু লিখো বন্ধু..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("দোস্ত ভাবছে..."):
            try:
                # সরাসরি ডাটা পাঠানো (কোনো লাইব্রেরি ছাড়া)
                payload = {
                    "contents": [{
                        "parts": [{"text": f"তুমি এহসানের বেস্ট ফ্রেন্ড। বাংলায় মজার কথা বলো। প্রশ্ন: {prompt}"}]
                    }]
                }
                headers = {'Content-Type': 'application/json'}
                
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                result = response.json()

                if response.status_code == 200:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    # যদি গুগল থেকে কোনো এরর আসে
                    st.error(f"এরর কোড: {response.status_code}")
                    st.write(result)
            except Exception as e:
                st.error(f"ইস বন্ধু! আবার সমস্যা: {e}")
