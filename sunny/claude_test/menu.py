import customtkinter as ctk

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.menu_label = ctk.CTkLabel(self, text="Main Menu", font=("Arial", 24))
        self.menu_label.pack(pady=20)

        buttons = [
            ("Personal Data", self.open_personal_data),
            ("Reports", self.open_reports),
            ("Settings", self.open_settings),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            button = ctk.CTkButton(self, text=text, command=command)
            button.pack(pady=10, padx=20, fill="x")

    def open_personal_data(self):
        print("Opening Personal Data")

    def open_reports(self):
        print("Opening Reports")

    def open_settings(self):
        print("Opening Settings")

    def logout(self):
        print("Logging out")