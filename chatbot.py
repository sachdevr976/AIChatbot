import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyttsx3
import speech_recognition as sr
import math

# --- Speech Setup ---
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio)
            return query
        except:
            return "Sorry, I didn't catch that."

def save_chat():
    with open("chat_history.txt", "a") as f:
        f.write(chat_area.get("1.0", tk.END) + "\n")
    messagebox.showinfo("Saved", "Chat history saved to chat_history.txt")

# --- Response Logic ---
def chatbot_response(user_input):
    user_input = user_input.lower()
    try:
        if '^' in user_input:
            parts = user_input.split('^')
            result = int(parts[0].strip()) ** int(parts[1].strip())
            return f"The answer is {result}."
        elif 'sqrt' in user_input:
            number = int(user_input.replace('sqrt', '').strip())
            result = math.sqrt(number)
            return f"The square root is {result:.2f}."
        elif '%' in user_input:
            parts = user_input.split('%')
            result = int(parts[0].strip()) % int(parts[1].strip())
            return f"The answer is {result}."
        elif '+' in user_input:
            parts = user_input.split('+')
            result = int(parts[0].strip()) + int(parts[1].strip())
            return f"The answer is {result}."
        elif '-' in user_input:
            parts = user_input.split('-')
            result = int(parts[0].strip()) - int(parts[1].strip())
            return f"The answer is {result}."
        elif 'x' in user_input or '*' in user_input:
            parts = user_input.replace('x', '*').split('*')
            result = int(parts[0].strip()) * int(parts[1].strip())
            return f"The answer is {result}."
        elif '/' in user_input:
            parts = user_input.split('/')
            result = int(parts[0].strip()) / int(parts[1].strip())
            return f"The answer is {result:.2f}."
    except:
        return "Please enter a valid math expression."

    responses = {
        'hello': 'Hello! How can I help you? 😊',
        'hi': 'Hi there! Ask me anything!',
        'how are you': 'I\'m doing great, thank you!',
        'bye': 'Goodbye! See you again! 👋',
        'thank you': 'You\'re welcome!',
        'what is your name': 'I am your friendly chatbot 🤖',
        'who created you': 'I was created by Mr Rahul Sachdev and Vardan Bajaj using Python!',
        'what can you do': 'I can chat, solve math, and more!',
        'tell me a joke': 'Why did the computer go to art school? Because it had a lot of draw functions!',
        'what is ai': 'AI stands for Artificial Intelligence — machines that think and learn!',
        'what is a chatbot': 'A chatbot is a computer program that talks with people.',
        'can you do math': 'Yes! Try asking something like 8 * 7 or sqrt 16.',
        'what is software engineering': 'Software engineering is the systematic approach to designing, developing, and maintaining software.',
        'what is computer science': 'Computer science is the study of computers, algorithms, and information.',
        'karachi is in which country': 'Karachi is in Pakistan.',
        'mumbai is in which country': 'Mumbai is in India.',
        'new york is in which country': 'New York is in the United States.',
        'tokyo is in which country': 'Tokyo is in Japan.',
        'who is vardan': 'Vardan is a naughty boy.',
        'who is kirtan': 'Kirtan is a good boy.',
        'who is rahul': 'Rahul is the father of Vardan and Kirtan. Also, he is my founder.',
        'who is the founder of iqra university': 'The founder of Iqra University is Mr. Late Hunaid Lakhani.',
        'who is teaching us software engineering': 'Dr. Ruzwan Munir is teaching us Software Engineering.',
        'who is teaching us python': 'Ma\'am Umat ul Shaiya is teaching us Python.',
        'who is teaching us dbms': 'Muhammad Sheeraz Iqbal is teaching us DBMS.',
        'who is teaching us agile software development': 'Muhammad Ahmed is teaching us Agile Software Development.',
        
        
        'who is vineet': 'Vineet is the brother of Rahul.',
        'who is father of rahul': 'The father of Rahul is Mr. Hargun Das.',
        'who is omee': 'Omee is a close friend of Rahul.',
        'what is cast of omee': 'Omee is from the Balani caste.',
        'who is sunny': 'Please do not ask about Sunny.',
        'tell me something about rahul': 'Rahul is an amazing person and a great friend. He is my creator, and I am always grateful to him! 😊',
        'rahul is': 'Rahul is a very hardworking and dedicated person. He is also a founder of this chatbot! 🧠',
        
       
        'who is kirsh': 'Kirsh is Rahul\'s brother. He is very hardworking and a really good person. 😊',
    }

    return responses.get(user_input, "I didn't understand that. Try something else or a math question like 9 * 5.")

# --- UI ---
root = tk.Tk()
root.title("✨ Smart AI Chatbot")
root.geometry("600x680")
root.configure(bg="#EAF2F8")

# Header
title = tk.Label(root, text="Smart AI Chatbot 🤖", font=("Helvetica", 22, "bold"), bg="#EAF2F8", fg="#2C3E50")
title.pack(pady=15)

# Chat Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12), bg="white", fg="#2C3E50", width=70, height=20, padx=10, pady=10, relief=tk.FLAT, bd=2)
chat_area.pack(pady=10)
chat_area.config(state=tk.DISABLED)
chat_area.tag_config("user", foreground="#2E86C1")
chat_area.tag_config("bot", foreground="#626567")

# Input Box
entry = tk.Entry(root, font=("Segoe UI", 12), width=40, relief=tk.FLAT, bd=2)
entry.pack(pady=5)

# Button Functions
def send():
    user_input = entry.get().strip()
    if not user_input:
        return
    response = chatbot_response(user_input)
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_input}la\n", "user")
    chat_area.insert(tk.END, f"Bot: {response}\n\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)
    entry.delete(0, tk.END)
    speak(response)

def mic_input():
    user_input = listen()
    response = chatbot_response(user_input)
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You (mic): {user_input}\n", "user")
    chat_area.insert(tk.END, f"Bot: {response}\n\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)
    speak(response)

# Button Panel
button_frame = tk.Frame(root, bg="#EAF2F8")
button_frame.pack(pady=15)

send_btn = tk.Button(button_frame, text="Send", command=send, font=("Segoe UI", 11), bg="#2ECC71", fg="white", padx=20, pady=5, relief=tk.FLAT)
send_btn.grid(row=0, column=0, padx=5)

mic_btn = tk.Button(button_frame, text="🎤 Speak", command=mic_input, font=("Segoe UI", 11), bg="#3498DB", fg="white", padx=20, pady=5, relief=tk.FLAT)
mic_btn.grid(row=0, column=1, padx=5)

save_btn = tk.Button(button_frame, text="💾 Save", command=save_chat, font=("Segoe UI", 11), bg="#F39C12", fg="white", padx=20, pady=5, relief=tk.FLAT)
save_btn.grid(row=0, column=2, padx=5)

root.mainloop()






