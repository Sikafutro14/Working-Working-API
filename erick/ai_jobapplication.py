import openai
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os


class ChatGPTApp:
    def __init__(self):
        # Load environment variables from .env file
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Conversation history and the initial system message
        self.system_role = "You are here to help the user to find a job"  # Define system role here
        self.messages = [{"role": "system", "content": self.system_role}]

        # Load the OpenAI API key from a file
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Set up OpenAI client
        self.setup_openai(self.api_key)
        self.setup_gui()


    # Function to set up OpenAI API
    def setup_openai(self, api_key):
        openai.api_key = api_key

    # Function to get a response from ChatGPT
    def get_chatgpt_response(self, messages):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    # Function to handle sending a message and displaying the response
    def send_message(self, event=None):
        user_input = self.user_entry.get()
        if not user_input:
            return

        # Display the user's message in the chat log
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"YOU: {user_input}\n")
        self.chat_log.config(state=tk.DISABLED)

        # Append the user's message to the conversation history
        self.messages.append({"role": "user", "content": user_input})

        # Get the response from ChatGPT
        response = self.get_chatgpt_response(self.messages)

        # Display ChatGPT's response in the chat log
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"CHAT GPT: {response}\n\n")
        self.chat_log.config(state=tk.DISABLED)

        # Append ChatGPT's response to the conversation history
        self.messages.append({"role": "assistant", "content": response})

        # Clear the input field
        self.user_entry.delete(0, tk.END)

    # Function to set up the GUI
    def setup_gui(self):
        # Initialize the GUI application
        self.root = tk.Tk()
        self.root.title("ChatGPT Interface")

        # Create a chat log window
        self.chat_log = ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create an entry box for the user to type messages
        self.user_entry = tk.Entry(self.root, font=("Arial", 12))
        self.user_entry.pack(padx=10, pady=10, fill=tk.X)

        # Bind the "Enter" key to send the message
        self.user_entry.bind("<Return>", self.send_message)

        # Create a button to send the message
        send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 12))
        send_button.pack(pady=5)

        # Run the main loop
        self.root.mainloop()

        # Conversation history and the initial system message
        self.system_role = "You are here to help the user to find a job"  # Define system role here
        self.messages = [{"role": "system", "content": self.system_role}]

        # Load the OpenAI API key from a file
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Set up OpenAI client
        self.setup_openai(self.api_key)

# Run the application
app = ChatGPTApp()