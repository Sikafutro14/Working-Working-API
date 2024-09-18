import customtkinter as ctk
from utils import create_label_entry

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.username = create_label_entry(self, "Username:", 0)
        self.password = create_label_entry(self, "Password:", 1)
        self.email = create_label_entry(self, "Email:", 2)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

    def register(self):
        # Implement registration logic here
        print("Registration attempted")