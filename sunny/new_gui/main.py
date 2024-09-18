import tkinter as tk
import customtkinter as ctk
import psycopg2
from dotenv import load_dotenv
import os
import openai

# Import your existing modules
from letter_generator import *
from letter import *
from main import *
from menu import *
import new_offer
from offer import *
from offers import *
import p_data
from offers import open_offers

# Load environment variables
load_dotenv()

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LoginRegisterFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color="gray10")
        self.on_login_success = on_login_success

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self, fg_color="gray15")
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.grid(row=0, column=0, padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=0, padx=20, pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, padx=20, pady=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, padx=20, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.on_login_success(username)
        else:
            print("Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Registered new user: {username}")
        self.on_login_success(username)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master, fg_color="gray10")
        self.username = username
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="gray15")
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="New Offer", command=self.new_offer)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="View Offers", command=self.view_offers)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Personal Data", command=self.show_personal_data)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="ChatGPT", command=self.chat_gpt)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_5 = ctk.CTkButton(self.sidebar_frame, text="Generate Resume", command=self.generate_resume)
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create textbox with white text on dark background
        self.textbox = ctk.CTkTextbox(self.main_frame, width=600, fg_color="gray25", text_color="white")
        self.textbox.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create entry and button frame
        self.entry_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.entry_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter command or query")
        self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(self.entry_frame, fg_color="transparent", border_width=2, text_color="white", text="Submit", command=self.submit_action)
        self.main_button_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def new_offer(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "Creating a new offer...\n")
        # Call the create_new_offer function from new_offer.py
        offer_result = new_offer.create_new_offer()
        self.textbox.insert("end", offer_result)


    def view_offers(self):
        """Displays the offers within the current window as text."""
        self.textbox.delete("1.0", "end")
        
        # Fetch the formatted offers string for the current user
        offers_str = open_offers(username=self.username)
        
        # Insert the fetched offers string into the textbox
        self.textbox.insert("end", offers_str)





    def show_personal_data(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "Loading personal data...\n")
        # Call the function from p_data.py
        personal_data = p_data.get_personal_data(user_id=self.username)
        self.textbox.insert("end", personal_data)


    def chat_gpt(self):
        prompt = self.entry.get()
        if not prompt:
            self.textbox.insert("end", "Please enter a prompt for ChatGPT.\n")
            return

        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", response.choices[0].message.content)
        except Exception as e:
            self.textbox.insert("end", f"Error: {str(e)}\n")

    def generate_resume(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "Generating resume...\n")
        resume_content = letter_generator.generate_resume()
        self.textbox.insert("end", resume_content)

    def submit_action(self):
        command = self.entry.get().lower()
        if command.startswith("select"):
            self.view_db_table()
        elif command.startswith("chat"):
            self.chat_gpt()
        else:
            self.textbox.delete("1.0", "end")
            self.textbox.insert("end", "Invalid command. Please try again.\n")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Application")
        self.geometry("1000x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginRegisterFrame(self, self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.dashboard_frame = None

    def on_login_success(self, username):
        self.login_frame.grid_forget()
        self.dashboard_frame = DashboardFrame(self, username)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()

