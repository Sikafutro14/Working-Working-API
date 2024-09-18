import customtkinter as ctk
from utils import create_label_entry

class PersonalDataFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.name = create_label_entry(self, "Full Name:", 0)
        self.dob = create_label_entry(self, "Date of Birth:", 1)
        self.address = create_label_entry(self, "Address:", 2)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_data)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_data(self):
        # Implement data saving logic here
        print("Personal data saved")