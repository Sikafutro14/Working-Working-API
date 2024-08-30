import customtkinter as ctk
import psycopg2
from openai import OpenAI
from tkinter import messagebox, filedialog
import os

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='hackingtrainer',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
        return None

def create_db():
    conn = connect_to_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Modules (
        ModuleID SERIAL PRIMARY KEY,
        Title TEXT,
        Content TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Challenges (
        ChallengeID SERIAL PRIMARY KEY,
        Title TEXT,
        Description TEXT,
        CodeSample TEXT
    );
    ''')
    conn.commit()
    conn.close()

class HackingTrainer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ethical Hacking Trainer")
        self.geometry("800x600")

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        # Initialize Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # ChatGPT Tab
        self.chatgpt_tab = self.tabview.add("ChatGPT Assistant")
        self.setup_chatgpt_tab()

        # Check if API key is set
        if not self.api_key:
            self.prompt_for_api_key()
        else:
            self.initialize_openai_client()

    def setup_chatgpt_tab(self):
        self.chatgpt_frame = ctk.CTkFrame(self.chatgpt_tab)
        self.chatgpt_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.prompt_entry = ctk.CTkEntry(self.chatgpt_frame, placeholder_text="Ask ChatGPT...", width=400)
        self.prompt_entry.pack(pady=10)

        self.ask_button = ctk.CTkButton(self.chatgpt_frame, text="Ask", command=self.ask_chatgpt)
        self.ask_button.pack(pady=10)

        self.response_box = ctk.CTkTextbox(self.chatgpt_frame, height=200, state="disabled")
        self.response_box.pack(pady=10, fill="both", expand=True)

        # Add API Key management button
        self.api_key_button = ctk.CTkButton(self.chatgpt_frame, text="Manage API Key", command=self.prompt_for_api_key)
        self.api_key_button.pack(pady=10)

    def prompt_for_api_key(self):
        file_path = filedialog.askopenfilename(title="Select API Key File", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_api_key = file.read().strip()
                if new_api_key:
                    self.api_key = new_api_key
                    self.initialize_openai_client()
                else:
                    messagebox.showerror("Invalid Input", "The selected file is empty. Please choose a file with a valid API key.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read the API key file: {e}")
        else:
            messagebox.showinfo("Cancelled", "API key file selection was cancelled.")

    def initialize_openai_client(self):
        try:
            self.client = OpenAI(api_key=self.api_key)
            messagebox.showinfo("Success", "API key loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI client: {e}")

    def ask_chatgpt(self):
        if not self.client:
            messagebox.showerror("Error", "OpenAI client is not initialized. Please load your API key.")
            self.prompt_for_api_key()
            return

        prompt = self.prompt_entry.get()
        if prompt:
            response = self.get_chatgpt_response(prompt)
            if response:
                self.response_box.configure(state="normal")
                self.response_box.insert("end", f"You: {prompt}\n\nChatGPT: {response}\n\n")
                self.response_box.configure(state="disabled")
                self.response_box.see("end")
                self.prompt_entry.delete(0, 'end')

    def get_chatgpt_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            messagebox.showerror("ChatGPT Error", f"Failed to get a response: {e}")
            return None

if __name__ == "__main__":
    create_db()  # Set up the database if not already set up
    app = HackingTrainer()
    app.mainloop()