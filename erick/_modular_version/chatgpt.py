import openai
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def help_chatgpt(user_id):
   
    load_dotenv()

    help_chat = tk.Tk()
    help_chat.title("ChatGPT Assistant")

    window_width = 1024
    window_height = 768
    
    center_window(help_chat, window_width, window_height)

    def on_back():
        help_chat.destroy()
        from menu import open_menu
        open_menu(user_id)

    api_key = os.getenv('OPENAI_API_KEY')
    messages = [{"role": "system", "content": "You are here to help the user find a job"}]

    chat_log = ScrolledText(help_chat, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(help_chat, font=("Arial", 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)

    def get_chatgpt_response(messages):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1.0,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def send_message(event=None):
        user_input = user_entry.get().strip()
        if user_input:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"YOU: {user_input}\n")
            chat_log.config(state=tk.DISABLED)
            messages.append({"role": "user", "content": user_input})

            response = get_chatgpt_response(messages)
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"CHAT GPT: {response}\n\n")
            chat_log.config(state=tk.DISABLED)

            messages.append({"role": "assistant", "content": response})
            user_entry.delete(0, tk.END)

    user_entry.bind("<Return>", send_message)
    send_button = tk.Button(help_chat, text="Send", command=send_message, font=("Arial", 12))
    send_button.pack(pady=5)

    back_button = tk.Button(help_chat, text="Back", command=on_back, font=("Arial", 12))
    back_button.pack(pady=5)

    help_chat.mainloop()