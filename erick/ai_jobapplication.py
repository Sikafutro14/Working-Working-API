import openai
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import os
from dotenv import load_dotenv
from resume_generator import generate_resume_letter, fetch_personal_info
from user_auth import register, login, get_db_connection


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
        result, user_id = login(username, password) 
        
        if result == "Login successful!":
            self.current_user_id = user_id
            self.root.destroy()
            self.details_entry_screen()
        else:
            self.display_message(result, "red")

    # Function to open registration screen
    def register_screen(self):
        self.root.destroy()  
        self.root = tk.Tk()  
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
            self.root.after(1000, self.show_login_screen)

    # Function to return to login screen after registration
    def show_login_screen(self):
        self.root.destroy()  
        self.login_screen()  

    # Function to display error or success message
    def display_message(self, message, color):
        tk.Label(self.root, text=message, fg=color).pack(pady=5)

    # Function to initialize the details entry screen
    def details_entry_screen(self):
        if self.details_exist_for_user():
            update = messagebox.askyesno("Details Exist", "Your details already exist. Do you want to update them?")
            if update:
                self.show_details_form(update=True) 
            else:
                self.jobfind_interface() 
        else:
            self.show_details_form(update=False)

    # Function to check if details exist for the current user
    def details_exist_for_user(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM details WHERE user_id = %s", (self.current_user_id,))
                result = cursor.fetchone()
                return result is not None  # True if data exists, False if not
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check existing details: {e}")
            return False

    def show_details_form(self, update=False):
        self.root = tk.Tk()
        self.root.title("Enter Personal Details" if not update else "Update Personal Details")

        tk.Label(self.root, text="Full Name:").pack(pady=5)
        self.full_name_entry = tk.Entry(self.root)
        self.full_name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Phone Number:").pack(pady=5)
        self.phone_number_entry = tk.Entry(self.root)
        self.phone_number_entry.pack(pady=5)

        tk.Label(self.root, text="Location:").pack(pady=5)
        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack(pady=5)

        tk.Label(self.root, text="Objective:").pack(pady=5)
        self.objective_entry = tk.Entry(self.root)
        self.objective_entry.pack(pady=5)

        # If updating, fetch and populate existing details
        if update:
            self.populate_existing_details()

        submit_button = tk.Button(self.root, text="Update" if update else "Submit", command=self.submit_details)
        submit_button.pack(pady=20)

        self.root.mainloop()

    def populate_existing_details(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT full_name, email, phone_number, location, objective FROM details WHERE user_id = %s", (self.current_user_id,))
                details = cursor.fetchone()

                if details:
                    full_name, email, phone_number, location, objective = details
                    self.full_name_entry.insert(0, full_name)
                    self.email_entry.insert(0, email)
                    self.phone_number_entry.insert(0, phone_number)
                    self.location_entry.insert(0, location)
                    self.objective_entry.insert(0, objective)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load existing details: {e}")

    def submit_details(self):
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        location = self.location_entry.get()
        objective = self.objective_entry.get()

        if not full_name or not email or not phone_number or not location or not objective:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Insert or update details
        self.insert_or_update_details(full_name, email, phone_number, location, objective)

    def insert_or_update_details(self, full_name, email, phone_number, location, objective):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                if self.details_exist_for_user():
                    # Update existing details
                    cursor.execute("""
                        UPDATE details 
                        SET full_name = %s, email = %s, phone_number = %s, location = %s, objective = %s
                        WHERE user_id = %s
                    """, (full_name, email, phone_number, location, objective, self.current_user_id))
                    messagebox.showinfo("Success", "Details updated successfully!")
                else:
                    # Insert new details
                    cursor.execute("""
                        INSERT INTO details (user_id, full_name, email, phone_number, location, objective)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (self.current_user_id, full_name, email, phone_number, location, objective))
                    messagebox.showinfo("Success", "Details submitted successfully!")

                conn.commit()
                self.root.destroy()  # Close the details entry window
                self.jobfind_interface()  # Go to the main interface
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit or update details: {e}")

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