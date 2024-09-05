import customtkinter
import tkinter



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.title("job_tracker")
app.geometry("400*400")

tabview = customtkinter.CTkTabview(app)
tabview.pack(padx=20,pady=20)












app.mainloop()