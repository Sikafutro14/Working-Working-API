import openai
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
from dotenv import load_dotenv
from resume_generator import generate_resume_letter, fetch_personal_info
from user_auth import verify_user, add_user

load_dotenv()
class JobFinderAI:
    def __init__(self):

        self.current_user_id = None
        # Load environment variables from .env file
        self.api_key = os.getenv('OPENAI_API_KEY')

        # Conversation history and the initial system message
        self.system_role = "You are here to help the user to find a job"  # Define system role here
        self.messages = [{"role": "system", "content": self.system_role}]

        # Set up OpenAI client
 
        self.setup_openai(self.api_key)
        self.login_screen()
        self.setup_gui()
        

    def login_screen(self):
        self.root = tk.Tk()
        self.root.title("Login")

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.pack(pady=20)

        register_button = tk.Button(self.root, text="Register", command=self.register_screen)
        register_button.pack(pady=5)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = verify_user(username, password)

        if user:
            self.root.destroy()  # Close the login window
            self.current_user_id = user['id']  # Store the user ID after successful login
            user_info = fetch_personal_info(self.current_user_id)
            if user_info:
                resume = generate_resume_letter(self.current_user_id)  # Pass user ID here
                self.display_resume(resume)
            else:
                tk.Label(self.root, text="Failed to fetch user information.", fg="red").pack(pady=5)
        else:
            tk.Label(self.root, text="Invalid credentials, try again.", fg="red").pack(pady=5)

    def register_screen(self):
        self.root.destroy()  # Close the login window
        self.root = tk.Tk()
        self.root.title("Register")

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        register_button = tk.Button(self.root, text="Register", command=self.register)
        register_button.pack(pady=20)

        self.root.mainloop()

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = add_user(username, email, password)
        tk.Label(self.root, text=result, fg="green" if "successfully" in result else "red").pack(pady=5)

        if "successfully" in result:
            self.root.after(2000, self.login_screen)
            self.root.destroy()


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
        self.root.title("JobFind Interface")

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

        # Create a button to generate the resume
        resume_button = tk.Button(self.root, text="Generate Resume", command=self.display_resume, font=("Arial", 12))
        resume_button.pack(pady=5)

        # Run the main loop
        self.root.mainloop()

    def display_resume(self, resume_text=None):
        if not resume_text:
            # Generate the resume if it wasn't provided
            user_info = fetch_personal_info(self.current_user_id)
            resume_text = generate_resume_letter(user_info)
        
        # Display the generated resume in the chat log
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"RESUME LETTER:\n{resume_text}\n\n")
        self.chat_log.config(state=tk.DISABLED)

# Run the application
app = JobFinderAI()

