import streamlit as st
import requests
import json

# ১. আপনার API Key (এটি একদম সঠিক আছে)
API_KEY = "AIzaSyAihcMxRjKtrLXCNaJbsCEPPQDLKWS-hF0"

# ২. সরাসরি এপিআই ইউআরএল (v1 ব্যবহার করা হয়েছে যাতে এরর না আসে)
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Ehesan's Buddy AI", page_icon="🤝")
st.title("🤝 এহসানের দোস্ত AI")

# আড্ডা মনে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের মেসেজগুলো দেখানো
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
                # সরাসরি রিকোয়েস্ট পাঠানো (সবচেয়ে নিরাপদ পদ্ধতি)
                payload = {
                    "contents": [{
                        "parts": [{"text": f"তুমি এহসানের বেস্ট ফ্রেন্ড। খুব মজার করে বাংলায় কথা বলো। প্রশ্ন: {prompt}"}]
                    }]
                }
                headers = {'Content-Type': 'application/json'}
                
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                result = response.json()

                if response.status_code == 200:
                    # উত্তরটি খুঁজে বের করা
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    # গুগল থেকে আসা এরর ডিটেইলস
                    st.error(f"এরর কোড: {response.status_code}")
                    st.json(result)
            except Exception as e:
                st.error(f"ইস বন্ধু! কারিগরি সমস্যা: {e}")
