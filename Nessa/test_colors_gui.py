from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("Nessa/CTK_THEMES/blue.json")

#creating the root as ctk
root = customtkinter.CTk()

root.title('Tkinter.com - CustomThinter Light Dark Modes')
#root.iconbitmap('images')
root.geometry('700x450')


mode ="dark"

def change_colors(choice):
    customtkinter.set_default_color_theme(choice)

def change():
    global mode
    if mode =="dark":
        customtkinter.set_appearance_mode("light")
        mode = "light"
        #clear text box
        my_text.delete(0.0, END)
        my_text.insert(END, "This light mode...")
    else: 
        customtkinter.set_appearance_mode("dark")
        mode ="dark"
        #clear text box
        my_text.delete(0.0, END)
        my_text.insert(END, "This Dark mode...")


my_text = customtkinter.CTkTextbox(root, width=600, height=300)
my_text.pack(pady=20)

my_button = customtkinter.CTkButton(root, text="change Light/Dark", command=change)
my_button.pack(pady=20)

colors = ["blue", "dark-blue","green"]
my_option = customtkinter.CTkOptionMenu(root, values=colors, command=change)
my_option.pack(pady=10)

my_progress =customtkinter.CTkProgressBar(root, orientation="horizontal")
my_progress.pack(pady=20)


root.mainloop()