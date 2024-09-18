import openai
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import os
from dotenv import load_dotenv
from resume_generator import generate_resume_letter
from user_auth import register, login, get_db_connection

load_dotenv()

class JobFinderAI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.current_user_id = None
        self.selected_offer_id = None  # Initialize selected_offer_id
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

        result, user_id = login(username, password) 
        
        if result == "Login successful!":
            self.current_user_id = user_id
            self.root.destroy()
            self.details_entry_screen()
        else:
            self.display_message(result, "red")

  
    def register_screen(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Register")
        self.create_register_widgets()
        self.root.mainloop()

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

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = register(username, email, password)
        self.display_message(result, "green" if "successfully" in result else "red")

        if "successfully" in result:
            self.root.after(1000, self.show_login_screen)

    def show_login_screen(self):
        self.root.destroy()
        self.login_screen()

    def display_message(self, message, color):
        tk.Label(self.root, text=message, fg=color).pack(pady=5)

    def details_entry_screen(self):
        if self.details_exist_for_user():
            update = messagebox.askyesno("Personal Info Exist", "Your personal info already exists. Do you want to update them?")
            if update:
                self.show_details_form(update=True)
            else:
                self.jobfind_interface()
        else:
            self.show_details_form(update=False)

    def details_exist_for_user(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM personal_info WHERE user_id = %s", (self.current_user_id,))
                result = cursor.fetchone()
                return result is not None  # True if data exists, False if not
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check existing personal_info: {e}")
            return False

    def show_details_form(self, update=False):
        self.root = tk.Tk()
        self.root.title("Enter Personal Info" if not update else "Update Personal Info")

        tk.Label(self.root, text="First Name:").pack(pady=5)
        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.root, text="Last Name:").pack(pady=5)
        self.last_name_entry = tk.Entry(self.root)
        self.last_name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Background:").pack(pady=5)
        self.background_entry = tk.Text(self.root, height=6, width=40, wrap=tk.WORD)
        self.background_entry.pack(pady=5)

        if update:
            self.populate_existing_details()

        submit_button = tk.Button(self.root, text="Update" if update else "Submit", command=self.submit_details)
        submit_button.pack(pady=20)

        self.root.mainloop()

    def populate_existing_details(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT first_name, last_name, email, background FROM personal_info WHERE user_id = %s", (self.current_user_id,))
                details = cursor.fetchone()

                if details:
                    first_name, last_name, email, background = details
                    self.first_name_entry.insert(0, first_name)
                    self.last_name_entry.insert(0, last_name)
                    self.email_entry.insert(0, email)
                    self.background_entry.insert(1.0, background)  # Corrected: Insert at line 1, column 0
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load existing personal info: {e}")

    def submit_details(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        background = self.background_entry.get("1.0", tk.END).strip() 

        if not first_name or not last_name or not email or not background:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.insert_or_update_details(first_name, last_name, email, background)

    def insert_or_update_details(self, first_name, last_name, email, background):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                if self.details_exist_for_user():
                    cursor.execute("""
                        UPDATE personal_info 
                        SET first_name = %s, last_name = %s, email = %s, background = %s
                        WHERE user_id = %s
                    """, (first_name, last_name, email, background, self.current_user_id))
                    messagebox.showinfo("Success", "Personal Info updated successfully!")
                else:
                    cursor.execute("""
                        INSERT INTO personal_info (user_id, first_name, last_name, email, background)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (self.current_user_id, first_name, last_name, email, background))
                    messagebox.showinfo("Success", "Personal info submitted successfully!")

                conn.commit()
                self.root.destroy()
                self.jobfind_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit or update Personal info: {e}")

    def jobfind_interface(self):
        self.root = tk.Tk()
        self.root.title("JobFind Interface")
        self.create_gui_widgets()
        self.root.mainloop()

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
        
        offer_button = tk.Button(self.root, text="Add Job Offer", command=self.show_offer_form, font=("Arial", 12))
        offer_button.pack(pady=5)

        select_offer_button = tk.Button(self.root, text="Select Job Offer", command=self.show_offer_selection, font=("Arial", 12))
        select_offer_button.pack(pady=5)

    def show_offer_form(self):
        self.offer_window = tk.Toplevel(self.root)
        self.offer_window.title("Add Job Offer")

        tk.Label(self.offer_window, text="Position:").pack(pady=5)
        self.position_entry = tk.Entry(self.offer_window)
        self.position_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Company:").pack(pady=5)
        self.company_entry = tk.Entry(self.offer_window)
        self.company_entry.pack(pady=5)

        tk.Label(self.offer_window, text="About Company:").pack(pady=5)
        self.about_entry = tk.Text(self.offer_window, height=5, width=40, wrap=tk.WORD)
        self.about_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Job Offer:").pack(pady=5)
        self.offer_entry = tk.Text(self.offer_window, height=5, width=40, wrap=tk.WORD)
        self.offer_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Application URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.offer_window)
        self.url_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Status (1 for active, 0 for inactive):").pack(pady=5)
        self.status_entry = tk.Entry(self.offer_window)
        self.status_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Response Received (1 for Yes, 0 for No):").pack(pady=5)
        self.response_entry = tk.Entry(self.offer_window)
        self.response_entry.pack(pady=5)

        submit_button = tk.Button(self.offer_window, text="Submit", command=self.submit_job_offer)
        submit_button.pack(pady=20)

    def submit_job_offer(self):
        position = self.position_entry.get()
        company = self.company_entry.get()
        about = self.about_entry.get("1.0", tk.END).strip()
        offer = self.offer_entry.get("1.0", tk.END).strip()
        url = self.url_entry.get()
        status = self.status_entry.get()
        response = self.response_entry.get()

        if not position or not company or not about or not offer or not url or not status or not response:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO offers (user_id, position, company, about, offer, url, status, response)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.current_user_id, position, company, about, offer, url, status, response))

                conn.commit()
                messagebox.showinfo("Success", "Job offer added successfully!")
                self.offer_window.destroy()  # Close the job offer window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit job offer: {e}")

    def fetch_job_offers(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, position, company
                    FROM offers
                    WHERE user_id = %s
                """, (self.current_user_id,))
                offers = cursor.fetchall()  # Fetch all offers for the user
                return offers
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch job offers: {e}")
            return []
    
    def show_offer_selection(self):
        self.offer_selection_window = tk.Toplevel(self.root)
        self.offer_selection_window.title("Select Job Offer")

        tk.Label(self.offer_selection_window, text="Select an offer to generate the resume for:", font=("Arial", 12)).pack(pady=10)

        # Fetch job offers from the database
        job_offers = self.fetch_job_offers()

        self.offer_var = tk.StringVar(value="")  # To store selected offer ID
        for offer in job_offers:
            offer_id, position, company = offer
            offer_text = f"Position: {position}, Company: {company}"
            tk.Radiobutton(self.offer_selection_window, text=offer_text, variable=self.offer_var, value=str(offer_id)).pack(anchor="w")

        submit_button = tk.Button(self.offer_selection_window, text="Submit", command=self.save_selected_offer)
        submit_button.pack(pady=10)
    
    def save_selected_offer(self):
        selected_offer_id = self.offer_var.get()
        if not selected_offer_id:
            messagebox.showerror("Error", "Please select a job offer.")
            return

        self.selected_offer_id = selected_offer_id  # Store the selected offer ID
        self.offer_selection_window.destroy()
        messagebox.showinfo("Success", "Job offer selected!")
    
    def display_resume(self):
        if not self.current_user_id:
            self.update_chat_log("No user logged in. Please log in first.\n")
            return

        if not self.selected_offer_id:
            self.update_chat_log("No job offer selected. Please select an offer first.\n")
            return

        resume_text = generate_resume_letter(self.current_user_id, self.selected_offer_id)  # Pass the offer ID
        self.update_chat_log(f"RESUME LETTER:\n{resume_text}\n\n")

    def get_chatgpt_response(self, messages):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    def send_message(self, event=None):
        user_input = self.user_entry.get()
        if user_input:
            self.update_chat_log(f"YOU: {user_input}\n")
            self.messages.append({"role": "user", "content": user_input})

            response = self.get_chatgpt_response(self.messages)
            self.update_chat_log(f"CHAT GPT: {response}\n\n")
            self.messages.append({"role": "assistant", "content": response})

            self.user_entry.delete(0, tk.END)

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message)
        self.chat_log.config(state=tk.DISABLED)

# Run the application
app = JobFinderAI()
