import customtkinter as ctk
from register import RegisterFrame
from login import LoginFrame
from p_data import PersonalDataFrame
from menu import MenuFrame

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Business Professional App")
        self.geometry("800x600")

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_view.add("Login")
        self.tab_view.add("Register")
        self.tab_view.add("Personal Data")
        self.tab_view.add("Menu")

        LoginFrame(self.tab_view.tab("Login")).pack(expand=True, fill="both", padx=10, pady=10)
        RegisterFrame(self.tab_view.tab("Register")).pack(expand=True, fill="both", padx=10, pady=10)
        PersonalDataFrame(self.tab_view.tab("Personal Data")).pack(expand=True, fill="both", padx=10, pady=10)
        MenuFrame(self.tab_view.tab("Menu")).pack(expand=True, fill="both", padx=10, pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()