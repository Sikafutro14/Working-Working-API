import openai
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to set up OpenAI API
def setup_openai(api_key):
    openai.api_key = api_key

# Function to get a response from ChatGPT
def get_chatgpt_response(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0,
        max_tokens=1000,
    )
    return response.choices[0].message.content

# Function to handle sending a message and displaying the response
def send_message(event=None):
    user_input = user_entry.get()
    if not user_input:
        return
    
    # Display the user's message in the chat log
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"YOU: {user_input}\n")
    chat_log.config(state=tk.DISABLED)

    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    # Get the response from ChatGPT
    response = get_chatgpt_response(messages)
    
    # Display ChatGPT's response in the chat log
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"CHAT GPT: {response}\n\n")
    chat_log.config(state=tk.DISABLED)

    # Append ChatGPT's response to the conversation history
    messages.append({"role": "assistant", "content": response})

    # Clear the input field
    user_entry.delete(0, tk.END)

# Function to set up the GUI
def setup_gui():
    global root, chat_log, user_entry

    # Initialize the GUI application
    root = tk.Tk()
    root.title("ChatGPT Interface")

    # Create a chat log window
    chat_log = ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create an entry box for the user to type messages
    user_entry = tk.Entry(root, font=("Arial", 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)

    # Bind the "Enter" key to send the message
    user_entry.bind("<Return>", send_message)

    # Create a button to send the message
    send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
    send_button.pack(pady=5)

    # Run the main loop
    root.mainloop()

# Conversation history and the initial system message
system_role = "You are here to help the user to find a job"  # Define system role here
messages = [{"role": "system", "content": system_role}]

# Load the OpenAI API key from a file
api_key = os.getenv('OPENAI_API_KEY')

# Set up OpenAI client
setup_openai(api_key)

# Set up and run the GUI
setup_gui()


