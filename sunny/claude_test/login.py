import customtkinter as ctk
from utils import create_label_entry

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.username = create_label_entry(self, "Username:", 0)
        self.password = create_label_entry(self, "Password:", 1)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        # Implement login logic here
        print("Login attempted")