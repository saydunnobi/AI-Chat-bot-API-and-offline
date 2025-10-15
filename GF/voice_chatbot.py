import tkinter as tk
from tkinter import scrolledtext
import threading
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# === CONFIG ===
genai.configure(api_key="Youer Api Key")
model = genai.GenerativeModel("API Model Name")

r = sr.Recognizer()
tts = pyttsx3.init()

# === FUNCTIONS ===
def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            chat_box.insert(tk.END, "\n🎤 Listening...\n")
            chat_box.see(tk.END)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            chat_box.insert(tk.END, f"You: {text}\n")
            chat_box.see(tk.END)
            return text
    except sr.UnknownValueError:
        chat_box.insert(tk.END, "Bot: Sorry, I didn’t catch that.\n")
        speak("Sorry, I didn’t catch that.")
    except Exception as e:
        chat_box.insert(tk.END, f"Error: {e}\n")
    return ""

def ask_gemini(text):
    try:
        response = model.generate_content(text)
        reply = response.text.strip()
        chat_box.insert(tk.END, f"Bot: {reply}\n")
        chat_box.see(tk.END)
        speak(reply)
    except Exception as e:
        chat_box.insert(tk.END, f"Error from Gemini: {e}\n")

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_box.insert(tk.END, f"You: {user_input}\n")
    entry.delete(0, tk.END)
    threading.Thread(target=ask_gemini, args=(user_input,)).start()

def voice_chat():
    threading.Thread(target=_voice_thread).start()

def _voice_thread():
    user_text = listen()
    if user_text:
        ask_gemini(user_text)

# === GUI SETUP ===
root = tk.Tk()
root.title("🎙️ Gemini Voice Chatbot")
root.geometry("600x500")
root.resizable(False, False)

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, font=("Arial", 10))
chat_box.pack(padx=10, pady=10)
chat_box.insert(tk.END, "🤖 Gemini Voice Chatbot Ready!\n")

entry_frame = tk.Frame(root)
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, width=50, font=("Arial", 11))
entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(entry_frame, text="Send", command=send_message, bg="#2196F3", fg="white")
send_button.grid(row=0, column=1, padx=5)

voice_button = tk.Button(root, text="🎤 Speak", command=voice_chat, bg="#4CAF50", fg="white", width=20)
voice_button.pack(pady=10)

root.mainloop()
