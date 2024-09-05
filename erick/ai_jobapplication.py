import openai
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
from dotenv import load_dotenv
from resume_generator import generate_resume_letter, fetch_personal_info
from user_auth import register, login

load_dotenv()

class JobFinderAI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.current_user_id = None
        self.system_role = "You are here to help the user to find a job"
        self.messages = [{"role": "system", "content": self.system_role}]
        self.setup_openai(self.api_key)
        self.login_screen()

    # Function to initialize OpenAI API
    def setup_openai(self, api_key):
        openai.api_key = api_key

    # Function to initialize login screen
    def login_screen(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.create_login_widgets()
        self.root.mainloop()

    # Function to create widgets for login screen
    def create_login_widgets(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.handle_login)
        login_button.pack(pady=20)

        register_button = tk.Button(self.root, text="Register", command=self.register_screen)
        register_button.pack(pady=5)

    # Function to handle user login
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Call the login function from user_auth
        result, user_id = login(username, password)  # Correct function call
        
        if result == "Login successful!":
            self.current_user_id = user_id
            self.root.destroy()
            self.jobfind_interface()
        else:
            self.display_message(result, "red")

    # Function to open registration screen
    def register_screen(self):
        self.root.destroy()  # Close login screen
        self.root = tk.Tk()  # Open a new window for registration
        self.root.title("Register")
        self.create_register_widgets()
        self.root.mainloop()

    # Function to create widgets for registration screen
    def create_register_widgets(self):
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

    # Function to handle user registration
    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = register(username, email, password)
        self.display_message(result, "green" if "successfully" in result else "red")

        if "successfully" in result:
            self.root.after(2000, self.show_login_screen)  # Show login screen after 2 seconds

    # Function to return to login screen after registration
    def show_login_screen(self):
        self.root.destroy()  # Close the registration window
        self.login_screen()  # Reopen the login screen

    # Function to display error or success message
    def display_message(self, message, color):
        tk.Label(self.root, text=message, fg=color).pack(pady=5)

    # Function to initialize the JobFind Interface
    def jobfind_interface(self):
        self.root = tk.Tk()
        self.root.title("JobFind Interface")
        self.create_gui_widgets()
        self.root.mainloop()

    # Function to create widgets for the main application
    def create_gui_widgets(self):
        self.chat_log = ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_entry = tk.Entry(self.root, font=("Arial", 12))
        self.user_entry.pack(padx=10, pady=10, fill=tk.X)
        self.user_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 12))
        send_button.pack(pady=5)

        resume_button = tk.Button(self.root, text="Generate Resume", command=self.display_resume, font=("Arial", 12))
        resume_button.pack(pady=5)

    # Function to get a response from ChatGPT
    def get_chatgpt_response(self, messages):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    # Function to send a message to ChatGPT and display the response
    def send_message(self, event=None):
        user_input = self.user_entry.get()
        if user_input:
            self.update_chat_log(f"YOU: {user_input}\n")
            self.messages.append({"role": "user", "content": user_input})

            response = self.get_chatgpt_response(self.messages)
            self.update_chat_log(f"CHAT GPT: {response}\n\n")
            self.messages.append({"role": "assistant", "content": response})

            self.user_entry.delete(0, tk.END)

    # Function to update chat log with messages
    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message)
        self.chat_log.config(state=tk.DISABLED)

    # Function to display generated resume
    def display_resume(self):
        if not self.current_user_id:
            self.update_chat_log("No user logged in. Please log in first.\n")
            return

        resume_text = generate_resume_letter(self.current_user_id)
        self.update_chat_log(f"RESUME LETTER:\n{resume_text}\n\n")


# Run the application
app = JobFinderAI()