import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import psycopg2
import os
#from openai import OpenAI

# Main application class
class ApplicationTrackerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Application Tracker")
        self.geometry("1000x800")

        # Set the default color theme to dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            self.initialize_openai_client()
        else:
            self.prompt_for_api_key()

        # Establish database connection
        self.db_connection = self.connect_to_database()
        if self.db_connection:
            self.db_cursor = self.db_connection.cursor()

        # Set up the frames for different sections
        self.setup_start_page()

    def execute_query(self, query, params=None):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect("dbname=job_app_db user=postgres password=password")
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def connect_to_database(self):
        try:
            connection = psycopg2.connect(
                database="job_app_db",
                user="postgres",
                password="password",
                host="localhost",
                port="5432"
            )
            messagebox.showinfo("Database", "Successfully connected to the database.")
            return connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
            return None

    def setup_start_page(self):
        self.start_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.start_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.start_frame, text="Application Tracker", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(self.start_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.start_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.start_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.new_account_button = ctk.CTkButton(self.start_frame, text="New Account", command=self.open_signup_page)
        self.new_account_button.pack(pady=10)

    def open_signup_page(self):
        self.start_frame.destroy()
        self.setup_signup_page()

    def setup_signup_page(self):
        self.signup_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.signup_frame.pack(fill="both", expand=True)

        self.signup_label = ctk.CTkLabel(self.signup_frame, text="Create New Account", font=("Arial", 24))
        self.signup_label.pack(pady=20)

        self.signup_username_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Username")
        self.signup_username_entry.pack(pady=10)

        self.signup_password_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Password", show="*")
        self.signup_password_entry.pack(pady=10)

        self.signup_repeat_password_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Repeat Password", show="*")
        self.signup_repeat_password_entry.pack(pady=10)

        self.create_account_button = ctk.CTkButton(self.signup_frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=10)

        self.back_to_login_button = ctk.CTkButton(self.signup_frame, text="Back to Login", command=self.back_to_login)
        self.back_to_login_button.pack(pady=10)

    def back_to_login(self):
        self.signup_frame.destroy()
        self.setup_start_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Placeholder for checking credentials
        self.open_main_interface()

    def create_account(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        repeat_password = self.signup_repeat_password_entry.get()
        # Placeholder for creating account logic
        self.back_to_login()

    def open_main_interface(self):
        self.start_frame.destroy()
        self.setup_main_interface()

    def setup_main_interface(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.main_frame.pack(fill="both", expand=True)

        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)

        self.chatgpt_tab = self.tabview.add("ChatGPT")
        self.resume_tab = self.tabview.add("Resume Generator")
        self.database_tab = self.tabview.add("Offer Database")

        self.setup_chatgpt_tab()
        self.setup_resume_tab()
        self.setup_database_tab()

    def setup_database_tab(self):
        self.database_frame = ctk.CTkFrame(self.database_tab, fg_color="gray20")
        self.database_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Entry for offer title
        self.offer_entry = ctk.CTkEntry(self.database_frame, placeholder_text="Offer Title")
        self.offer_entry.pack(pady=10)

        # Frame for buttons
        self.buttons_frame = ctk.CTkFrame(self.database_frame, fg_color="gray20")
        self.buttons_frame.pack(pady=10, fill="x")

        # Create, Update, Delete, and Refresh buttons
        self.create_offer_button = ctk.CTkButton(self.buttons_frame, text="Create Offer", command=self.create_offer)
        self.create_offer_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_offer_button = ctk.CTkButton(self.buttons_frame, text="Update Offer", command=self.update_offer)
        self.update_offer_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_offer_button = ctk.CTkButton(self.buttons_frame, text="Delete Offer", command=self.delete_offer)
        self.delete_offer_button.grid(row=0, column=2, padx=5, pady=5)

        self.refresh_button = ctk.CTkButton(self.buttons_frame, text="Refresh List", command=self.display_offers)
        self.refresh_button.grid(row=0, column=3, padx=5, pady=5)

        # Listbox for displaying offers
        self.offers_listbox = tk.Listbox(self.database_frame)
        self.offers_listbox.pack(pady=10, fill="both", expand=True)

        self.display_offers()

    def fetch_offers(self):
        connection = None
        cursor = None
        try:
            query = "SELECT * FROM offers"
            connection = self.db_connection
            cursor = self.db_cursor
            cursor.execute(query)
            offers = cursor.fetchall()
            return offers
        except Exception as e:
            print(f"Failed to fetch offers: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def create_offer(self):
        try:
            query = """
            INSERT INTO offers (user_id, company, department, offer_url, company_description, offer_text, status, response)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            connection = self.db_connection
            cursor = self.db_cursor
            cursor.execute(query, (
                1,  # Placeholder values
                "Company",
                "Department",
                "http://offer.url",
                "Company Description",
                "Offer Text",
                1,
                True
            ))
            connection.commit()
            print("Offer created successfully.")
        except Exception as e:
            print(f"Failed to create offer: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_offer(self):
        try:
            query = """
            UPDATE offers
            SET user_id = %s, company = %s, department = %s, offer_url = %s, company_description = %s,
                offer_text = %s, status = %s, response = %s
            WHERE id = %s
            """
            connection = self.db_connection
            cursor = self.db_cursor
            cursor.execute(query, (
                1,  # Placeholder values
                "Company",
                "Department",
                "http://offer.url",
                "Company Description",
                "Offer Text",
                1,
                True,
                1  # Placeholder Offer ID to update
            ))
            connection.commit()
            print("Offer updated successfully.")
        except Exception as e:
            print(f"Failed to update offer: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_offer(self):
        try:
            query = "DELETE FROM offers WHERE id = %s"
            connection = self.db_connection
            cursor = self.db_cursor
            cursor.execute(query, (1,))  # Placeholder Offer ID
            connection.commit()
            print("Offer deleted successfully.")
        except Exception as e:
            print(f"Failed to delete offer: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def display_offers(self):
        offers = self.fetch_offers()

        self.offers_listbox.delete(0, tk.END)

        if offers:
            for offer in offers:
                self.offers_listbox.insert(tk.END, f"ID: {offer[0]}, Company: {offer[2]}, Department: {offer[3]}")
        else:
            self.offers_listbox.insert(tk.END, "No offers available")

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

    def setup_chatgpt_tab(self):
        self.chatgpt_frame = ctk.CTkFrame(self.chatgpt_tab, fg_color="gray20")
        self.chatgpt_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.prompt_entry = ctk.CTkEntry(self.chatgpt_frame, placeholder_text="Ask ChatGPT...", width=400)
        self.prompt_entry.pack(pady=10)

        self.ask_button = ctk.CTkButton(self.chatgpt_frame, text="Ask", command=self.ask_chatgpt)
        self.ask_button.pack(pady=10)

        self.response_box = ctk.CTkTextbox(self.chatgpt_frame, height=200, state="disabled", fg_color="white", text_color="black")
        self.response_box.pack(pady=10, fill="both", expand=True)

        self.setup_context_menus()

    def setup_resume_tab(self):
        self.resume_frame = ctk.CTkFrame(self.resume_tab, fg_color="gray20")
        self.resume_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.offer_link_entry = ctk.CTkEntry(self.resume_frame, placeholder_text="Paste offer link here...")
        self.offer_link_entry.pack(pady=10)

        self.generate_resume_button = ctk.CTkButton(self.resume_frame, text="Generate Resume", command=self.generate_resume)
        self.generate_resume_button.pack(pady=10)

        self.resume_response_box = ctk.CTkTextbox(self.resume_frame, height=200, state="disabled", fg_color="white", text_color="black")
        self.resume_response_box.pack(pady=10, fill="both", expand=True)

    def generate_resume(self):
        offer_link = self.offer_link_entry.get()
        response = "Generated resume based on offer link."
        self.display_resume_response(response)

    def display_resume_response(self, response):
        self.resume_response_box.configure(state="normal")
        self.resume_response_box.insert(tk.END, response + "\n")
        self.resume_response_box.configure(state="disabled")

    def setup_context_menus(self):
        self.context_menu_prompt_entry = tk.Menu(self, tearoff=0)
        self.context_menu_prompt_entry.add_command(label="Copy", command=self.copy_text_prompt_entry)
        self.context_menu_prompt_entry.add_command(label="Paste", command=self.paste_text_prompt_entry)

        self.prompt_entry.bind("<Button-3>", self.show_context_menu_prompt_entry)

        self.context_menu_response_box = tk.Menu(self, tearoff=0)
        self.context_menu_response_box.add_command(label="Copy", command=self.copy_text_response_box)
        self.context_menu_response_box.add_command(label="Paste", command=self.paste_text_response_box)

        self.response_box.bind("<Button-3>", self.show_context_menu_response_box)

    def copy_text_prompt_entry(self):
        try:
            selected_text = self.prompt_entry.get()
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {e}")

    def paste_text_prompt_entry(self):
        try:
            clipboard_text = self.clipboard_get()
            self.prompt_entry.insert(tk.INSERT, clipboard_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste text: {e}")

    def copy_text_response_box(self):
        try:
            selected_text = self.response_box.get("1.0", tk.END)
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {e}")

    def paste_text_response_box(self):
        try:
            clipboard_text = self.clipboard_get()
            self.response_box.configure(state="normal")
            self.response_box.insert(tk.END, clipboard_text)
            self.response_box.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste text: {e}")

    def show_context_menu_prompt_entry(self, event):
        self.context_menu_prompt_entry.post(event.x_root, event.y_root)

    def show_context_menu_response_box(self, event):
        self.context_menu_response_box.post(event.x_root, event.y_root)

if __name__ == "__main__":
    app = ApplicationTrackerApp()
    app.mainloop()


