import streamlit as st
from openai import OpenAI

st.title("🤖 Man in Chatbot")

# Create client using your OpenAI API key
client = OpenAI(api_key="AIzaSyA3uAgSmSEmz6eR9S7pBYMzVFOuc6aeGZg")

# Store messages in session (memory)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are an AI learning assistant that helps users understand AI concepts."}]

user_input = st.text_input("You:", placeholder="Ask me anything about AI...")

if st.button("Send"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.write("🤖:", reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
