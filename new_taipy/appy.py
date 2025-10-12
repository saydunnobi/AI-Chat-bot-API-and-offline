import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.title("🤖 Offline AI Chatbot (Hugging Face Model)")

# Choose model: GPT-2, Mistral, or LLaMA
model_name = "gpt2"  # try "mistralai/Mistral-7B-v0.1" if you have strong GPU

@st.cache_resource
def load_model(name):
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name)
    return tokenizer, model

tokenizer, model = load_model(model_name)

# Keep conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

user_input = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send") and user_input:
    st.session_state.chat_history += f"\nYou: {user_input}\nAI:"
    inputs = tokenizer(st.session_state.chat_history, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        pad_token_id=tokenizer.eos_token_id
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply_text = reply.split("AI:")[-1].strip()
    st.session_state.chat_history += f" {reply_text}"
    st.text_area("Chat History", st.session_state.chat_history, height=400)
