import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, Menu
from CTkToolTip import CTkToolTip
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ResumeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Resume Writer AI")
        self.geometry("1400x1200")

        # Custom color scheme
        self.dark_blue = "#00274D"
        self.white = "#FFFFFF"
        self.accent_color = "#0056A0"
        self.text_color = "#E6E6E6"
        self.shade = "#5A7D9A"  # A medium blue-gray shade

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.configure(fg_color=self.dark_blue)

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        # Initialize OpenAI client and database connection
        self.gpt_app = ApplicationTrackerGPT(self)
        self.db_app = ApplicationTrackerOffers(self)

        '''self.db_app.create_offer(offer_title)
        self.db_app.update_offer(offer_id, new_title)
        self.db_app.delete_offer(offer_id)
        offers = self.db_app.fetch_offers()'''




        # Initialize the application
        self.setup_main_interface()

        
        self.initialize_database()

    def setup_main_interface(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color=self.dark_blue)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=self.accent_color)
        header_frame.pack(fill="x", pady=(0, 20))

        header_label = ctk.CTkLabel(header_frame, text="Resume Writer AI", font=("Roboto", 24, "bold"), text_color=self.white)
        header_label.pack(pady=10)

        # Tabview
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color=self.accent_color, segmented_button_fg_color=self.dark_blue, segmented_button_unselected_color=self.accent_color)
        self.tabview.pack(fill="both", expand=True)

        self.offer_management_tab = self.tabview.add("Offer Management")
        self.ask_chatgpt_tab = self.tabview.add("Ask ChatGPT")

        # Resume Generation Tab
        self.resume_generation_tab = self.tabview.add("Resume Generation")
        self.setup_resume_generation_tab()  # Call the setup function for the new tab

        self.setup_offer_management_tab()
        self.setup_ask_chatgpt_tab()

        # Bind the context menu to the prompt_entry
        self.prompt_entry.bind("<Button-3>", self.show_context_menu)

    def initialize_database(self):
        if self.db_app:
            self.db_app.create_offers_table()
            # Optionally populate the database with fake data
            # self.db_app.populate_db_with_fake_data()

    def setup_offer_management_tab(self):
        self.offer_management_tab.grid_columnconfigure(0, weight=1)
        self.offer_management_tab.grid_rowconfigure(1, weight=1)
        
        # Input fields for ID, Company, and Title
        self.id_entry = ctk.CTkEntry(self.offer_management_tab, placeholder_text="Offer ID", width=300, height=40, 
                                    font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.id_entry.grid(row=0, column=0, padx=20, pady=(10, 5))

        self.company_entry = ctk.CTkEntry(self.offer_management_tab, placeholder_text="Company", width=300, height=40, 
                                        font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.company_entry.grid(row=1, column=0, padx=20, pady=5)

        self.title_entry = ctk.CTkEntry(self.offer_management_tab, placeholder_text="Offer Title", width=300, height=40, 
                                        font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.title_entry.grid(row=2, column=0, padx=20, pady=10)

        create_offer_button = ctk.CTkButton(self.offer_management_tab, text="Create Offer", command=self.create_offer)
        create_offer_button.grid(row=3, column=0, pady=(0, 10))

        # Top frame for buttons
        top_frame = ctk.CTkFrame(self.offer_management_tab, fg_color="transparent")
        top_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=20, pady=(10, 20))
        top_frame.grid_columnconfigure(0, weight=1)

        # Buttons
        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, sticky="ew")

        buttons = [
            ("Create", self.create_offer),
            ("Update", self.update_offer),
            ("Delete", self.delete_offer),
            ("Refresh", self.display_offers)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(button_frame, text=text, command=command, width=100, height=40, 
                                font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.white,
                                border_width=2, border_color=self.white)
            btn.grid(row=0, column=i, padx=5)
            CTkToolTip(btn, message=f"{text} offer")

        # Create Treeview for PostgreSQL-like display
        self.tree = ttk.Treeview(self.offer_management_tab, columns=("id", "company", "title"), show="headings")
        
        # Define column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100, anchor="w")

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(self.offer_management_tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Grid layout for Treeview and scrollbar
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=(20, 0), pady=10)
        vsb.grid(row=4, column=2, sticky="ns", pady=10)

        # Configure row and column weights
        self.offer_management_tab.grid_rowconfigure(4, weight=1)
        self.offer_management_tab.grid_columnconfigure(0, weight=1)

        # Style configuration for Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=self.white,
                        foreground=self.dark_blue,
                        rowheight=25,
                        fieldbackground=self.white)
        style.map('Treeview', background=[('selected', self.accent_color)])
        style.configure("Treeview.Heading",
                        background=self.accent_color,
                        foreground=self.white,
                        relief="flat")
        style.map("Treeview.Heading",
                background=[('active', self.shade)])





    def create_table_headers(self):
        headers = ["ID", "Company", "Department", "Offer URL", "Company Description", "Offer Text", "Status", "Response", "Title"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=("Roboto", 12, "bold"), 
                                 width=120, height=30, fg_color=self.accent_color, text_color=self.white)
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            self.table_frame.grid_columnconfigure(i, weight=1)

    def create_offer(self):
        offer_id = self.id_entry.get()
        company = self.company_entry.get()
        title = self.title_entry.get()

        if self.db_app:
            # Call method to create offer in the database
            self.db_app.create_offer(offer_id, company, title)
            self.display_offers()  # Update the display after creating an offer
        else:
            messagebox.showerror("Error", "Database connection not initialized")




    def update_offer(self):
        selected_item = self.tree.selection()  # Get selected offer from the table
        if selected_item:
            offer_id = self.tree.item(selected_item)["values"][0]  # Get offer ID from the selected item
            new_title = self.offer_title_entry.get()  # Get new title from the input field
            if self.db_app:
                self.db_app.update_offer(offer_id, new_title)
                self.display_offers()  # Update the display after updating an offer
            else:
                messagebox.showerror("Error", "Database connection not initialized")



    def delete_offer(self):
        selected_item = self.tree.selection()  # Get selected offer from the table
        if selected_item:
            offer_id = self.tree.item(selected_item)["values"][0]  # Get offer ID from the selected item
            if self.db_app:
                self.db_app.delete_offer(offer_id)
                self.display_offers()  # Update the display after deleting an offer
            else:
                messagebox.showerror("Error", "Database connection not initialized")



    def display_offers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        offers = self.db_app.fetch_offers()

        for offer in offers:
            self.tree.insert("", "end", values=offer)


        # Fetch offers from the database
        offers = self.db_app.fetch_offers()

        # Insert new data
        for offer in offers:
            self.tree.insert("", "end", values=offer)

    def update_offers_display(self, offers):
        # Clear existing data
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add new rows to the table
        if offers:
            for i, offer in enumerate(offers, start=1):
                for j, data in enumerate(offer):
                    label = ctk.CTkLabel(self.scrollable_frame, text=str(data), font=("Roboto", 12),
                                         width=120, height=30, fg_color=self.white, text_color=self.dark_blue)
                    label.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                    self.scrollable_frame.grid_columnconfigure(j, weight=1)
        else:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="No offers available", font=("Roboto", 12), text_color=self.dark_blue)
            empty_label.grid(row=1, column=0, columnspan=9, pady=20)

    
    def setup_resume_generation_tab(self):
        # Main frame for the tab
        resume_frame = ctk.CTkFrame(self.resume_generation_tab, fg_color="transparent")
        resume_frame.pack(fill="both", expand=True, pady=20)

         # Create a label and entry for User ID
        user_id_label = ctk.CTkLabel(resume_frame, text="User ID:", font=("Roboto", 14), text_color=self.white)
        user_id_label.pack(pady=(10, 0))

        self.user_id_entry = ctk.CTkEntry(resume_frame, placeholder_text="Enter your User ID", width=200, height=40, 
                                        font=("Roboto", 14), fg_color=self.white, text_color=self.dark_blue)
        self.user_id_entry.pack(pady=(0, 20))

        self.generate_resume_button = ctk.CTkButton(resume_frame, text="Generate Resume", command=self.generate_resume, width=150, height=40,
                                                    font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.shade)
        self.generate_resume_button.pack(pady=(10, 20))

        # Output Section for the resume
        self.resume_output_box = ctk.CTkTextbox(resume_frame, fg_color=self.white, text_color=self.dark_blue,
                                                font=("Roboto", 12), wrap="word", state="normal")
        self.resume_output_box.pack(fill="both", expand=True, pady=(0, 20))



    def generate_resume(self):
        user_id = self.user_id_entry.get()  # Retrieve the User ID from the input field

        if not user_id:
            self.show_error_message("Please enter a User ID.")
            return

        # Call the resume generation function, possibly from `sunny_resume_gen.py`
        resume = generate_resume_letter(user_id)  # This is presumably in your `sunny_resume_gen.py`

        if resume:
            self.resume_output_box.delete(1.0, "end")
            self.resume_output_box.insert("end", resume)
        else:
            self.show_error_message("Failed to generate resume.")


    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)

    def show_info_message(self, message):
        tk.messagebox.showinfo("Info", message)


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

        self.ask_button = ctk.CTkButton(input_frame, text="Ask ChatGPT", command=self.gpt_app.ask_chatgpt, 
                                        width=120, height=40, font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.shade,
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
        widget = event.widget
        self.context_menu.entryconfigure("Copy", state="normal" if widget.selection_present() else "disabled")
        self.context_menu.tk_popup(event.x_root, event.y_root)

    
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

if __name__ == "__main__":
    app = ResumeApp()
    app.gpt_app.initialize_openai_client()  # Initialize OpenAI client
    app.mainloop()

