import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import psycopg2
import os
from openai import OpenAI
from faker import Faker
from CTkToolTip import CTkToolTip

class ApplicationTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Application Tracker")
        self.geometry("1200x800")

        # Custom color scheme
        self.dark_blue = "#00274D"
        self.white = "#FFFFFF"
        self.accent_color = "#0056A0"
        self.text_color = "#E6E6E6"

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.configure(fg_color=self.dark_blue)

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            self.initialize_openai_client()
        else:
            self.prompt_for_api_key()

        self.db_connection = self.connect_to_database()
        if self.db_connection:
            self.db_cursor = self.db_connection.cursor()
            self.create_offers_table()  # Create the table if it doesn't exist

        self.setup_main_interface()

    def setup_main_interface(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color=self.dark_blue)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=self.accent_color)
        header_frame.pack(fill="x", pady=(0, 20))

        header_label = ctk.CTkLabel(header_frame, text="Application Tracker", font=("Roboto", 24, "bold"), text_color=self.white)
        header_label.pack(pady=10)

        # Tabview
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color=self.accent_color, segmented_button_fg_color=self.dark_blue, 
                                      segmented_button_selected_color=self.white, segmented_button_unselected_color=self.accent_color)
        self.tabview.pack(fill="both", expand=True)

        self.offer_management_tab = self.tabview.add("Offer Management")
        self.ask_chatgpt_tab = self.tabview.add("Ask ChatGPT")

        self.setup_offer_management_tab()
        self.setup_ask_chatgpt_tab()

    def setup_offer_management_tab(self):
        # Top frame for input and buttons
        top_frame = ctk.CTkFrame(self.offer_management_tab, fg_color="transparent")
        top_frame.pack(fill="x", pady=20)

        # Offer title input
        self.offer_entry = ctk.CTkEntry(top_frame, placeholder_text="Offer Title", width=300, height=40, 
                                        font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.offer_entry.pack(side="left", padx=(0, 20))

        # Copy button for offer title
        copy_offer_btn = ctk.CTkButton(top_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.offer_entry.get()),
                                       width=60, height=40, fg_color=self.accent_color, hover_color=self.white)
        copy_offer_btn.pack(side="left")
        CTkToolTip(copy_offer_btn, message="Copy offer title")

        # Buttons
        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.pack(side="right")

        buttons = [
            ("Create", self.create_offer),
            ("Update", self.update_offer),
            ("Delete", self.delete_offer),
            ("Refresh", self.display_offers)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(button_frame, text=text, command=command, width=100, height=40, 
                                font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.white,
                                border_width=2, border_color=self.white)  # Added border
            btn.pack(side="left", padx=5)
            CTkToolTip(btn, message=f"{text} offer")

        # Offer list
        list_frame = ctk.CTkFrame(self.offer_management_tab, fg_color=self.white)
        list_frame.pack(fill="both", expand=True, pady=(20, 0))

        self.offers_listbox = tk.Listbox(list_frame, bg=self.white, fg=self.dark_blue, font=("Roboto", 12), 
                                         selectbackground=self.accent_color, relief="flat", highlightthickness=0)
        self.offers_listbox.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        scrollbar = ctk.CTkScrollbar(list_frame, command=self.offers_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.offers_listbox.config(yscrollcommand=scrollbar.set)

        # Add right-click context menu for copy/paste
        self.create_context_menu()

    def setup_ask_chatgpt_tab(self):
        chat_frame = ctk.CTkFrame(self.ask_chatgpt_tab, fg_color="transparent")
        chat_frame.pack(fill="both", expand=True, pady=20)

        # Chat history
        self.response_box = ctk.CTkTextbox(chat_frame, fg_color=self.white, text_color=self.dark_blue, 
                                           font=("Roboto", 12), wrap="word", state="normal")
        self.response_box.pack(fill="both", expand=True, pady=(0, 20))

        # Input area
        input_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        self.prompt_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter your prompt for ChatGPT", 
                                         height=40, font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.prompt_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        copy_prompt_btn = ctk.CTkButton(input_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.prompt_entry.get()),
                                        width=60, height=40, fg_color=self.accent_color, hover_color=self.white,
                                        border_width=2, border_color=self.white)  # Added border
        copy_prompt_btn.pack(side="left", padx=(0, 10))
        CTkToolTip(copy_prompt_btn, message="Copy prompt")

        self.ask_button = ctk.CTkButton(input_frame, text="Ask ChatGPT", command=self.ask_chatgpt, 
                                        width=120, height=40, font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.white,
                                        border_width=2, border_color=self.white)  # Added border
        self.ask_button.pack(side="right")
        CTkToolTip(self.ask_button, message="Send prompt to ChatGPT")

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

    def create_context_menu(self):
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selection)
        self.context_menu.add_command(label="Paste", command=self.paste_selection)

        self.bind("<Button-3>", self.show_context_menu)  # Bind right-click

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selection(self):
        try:
            selected_text = self.focus_get().get(tk.SEL_FIRST, tk.SEL_LAST)
            self.copy_to_clipboard(selected_text)
        except:
            messagebox.showwarning("No Selection", "No text selected to copy.")

    def paste_selection(self):
        try:
            text = self.clipboard_get()
            self.focus_get().insert(tk.INSERT, text)
        except:
            messagebox.showwarning("Paste Error", "Failed to paste text.")

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

    def connect_to_database(self):
        try:
            # Update with your actual database credentials
            conn = psycopg2.connect(
                dbname="job_app_db",
                user="postgres",
                password="password",
                host="localhost",
                port="5432"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
            return None
        
    def create_offers_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
        """
        self.execute_query(create_table_query)

    

    def execute_query(self, query, params=None):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, params)
                self.db_connection.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to execute query: {e}")

    def fetch_offers(self):
        try:
            self.db_cursor.execute("SELECT * FROM offers")
            return self.db_cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch offers: {e}")
            return []

    def create_offer(self):
        title = self.offer_entry.get().strip()
        if title:
            self.execute_query("INSERT INTO offers (title) VALUES (%s)", (title,))
            self.display_offers()
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def update_offer(self):
        # For simplicity, assume offer_id is fetched from listbox or another input field.
        offer_id = 1
        title = self.offer_entry.get().strip()
        if title:
            self.execute_query("UPDATE offers SET title = %s WHERE id = %s", (title, offer_id))
            self.display_offers()
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def delete_offer(self):
        # For simplicity, assume offer_id is fetched from listbox or another input field.
        offer_id = 1
        self.execute_query("DELETE FROM offers WHERE id = %s", (offer_id,))
        self.display_offers()

    def display_offers(self):
        offers = self.fetch_offers()
        self.offers_listbox.delete(0, tk.END)
        if offers:
            for offer in offers:
                offer_str = f"ID: {offer[0]}, Title: {offer[1]}"
                self.offers_listbox.insert(tk.END, offer_str)
        else:
            self.offers_listbox.insert(tk.END, "No offers available")

    def populate_db_with_fake_data(self):
        fake = Faker()
        for _ in range(10):
            title = fake.company()  # Generate a fake company name as the offer title
            self.execute_query("INSERT INTO offers (title) VALUES (%s)", (title,))

if __name__ == "__main__":
    app = ApplicationTrackerApp()
    app.populate_db_with_fake_data()  # Populate DB with fake data
    app.mainloop()
