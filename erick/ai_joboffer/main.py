import openai
import os
import tkinter as tk
from tkinter import messagebox
from user_auth import login, register
from job_offer import JobOfferHandler

class JobFinderAI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.current_user_id = None
        self.setup_openai(self.api_key)
        self.login_screen()

    def setup_openai(self, api_key):
        openai.api_key = api_key

    def login_screen(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.create_login_widgets()
        self.root.mainloop()

    def create_login_widgets(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_screen).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        msg, user_id = login(username, password)
        if user_id:
            self.current_user_id = user_id
            self.root.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Login Failed", msg)

    def register_screen(self):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")

        tk.Label(self.register_window, text="Username:").pack(pady=5)
        self.reg_username_entry = tk.Entry(self.register_window)
        self.reg_username_entry.pack(pady=5)

        tk.Label(self.register_window, text="Email:").pack(pady=5)
        self.reg_email_entry = tk.Entry(self.register_window)
        self.reg_email_entry.pack(pady=5)

        tk.Label(self.register_window, text="Password:").pack(pady=5)
        self.reg_password_entry = tk.Entry(self.register_window, show='*')
        self.reg_password_entry.pack(pady=5)

        tk.Button(self.register_window, text="Register", command=self.register).pack(pady=5)

    def register(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        msg = register(username, email, password)
        messagebox.showinfo("Registration", msg)
        if "successful" in msg:
            self.register_window.destroy()

    def open_main_app(self):
        self.main_app = tk.Tk()
        self.main_app.title("Job Finder App")
        self.job_offer_handler = JobOfferHandler(self.main_app, self.current_user_id)
        self.main_app.mainloop()

if __name__ == "__main__":
    JobFinderAI()
