import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, Menu
from CTkToolTip import CTkToolTip
import openai
from sunny_gpt import *
from sunny_offers import *
import os
from dotenv import load_dotenv

#Load environment variables from.env file
load_dotenv()

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
        self.shade = "#5A7D9A"  # A medium blue-gray shade

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.configure(fg_color=self.dark_blue)

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        # Initialize OpenAI client and database connection
        self.gpt_app = ApplicationTrackerGPT(self)
        self.db_app = ApplicationTrackerOffers(self)

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
        self.tabview = ctk.CTkTabview(self.main_frame, fg_color=self.accent_color, segmented_button_fg_color=self.dark_blue,  segmented_button_unselected_color=self.accent_color)
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

        # Buttons
        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.pack(side="right")

        buttons = [
            ("Create", self.db_app.create_offer),
            ("Update", self.db_app.update_offer),
            ("Delete", self.db_app.delete_offer),
            ("Refresh", self.db_app.display_offers)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(button_frame, text=text, command=command, width=100, height=40, 
                                font=("Roboto", 12), fg_color=self.accent_color, hover_color=self.shade,
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

if __name__ == "__main__":
    app = ApplicationTrackerApp()
    app.gpt_app.initialize_openai_client()  # Initialize OpenAI client
    app.db_app.create_offers_table()  # Create the offers table if it doesn't exist
    app.mainloop()
