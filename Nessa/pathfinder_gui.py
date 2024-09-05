import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from PIL import Image, ImageTk

# Function to register user details
def register_user():
    def save_details():
        user_data = {
            "name": name_entry.get(),
            "dob": dob_entry.get(),
            "country": country_entry.get(),
            "city": city_entry.get(),
            "gender": gender_var.get(),
            "username": username_entry.get(),
            "password": password_entry.get()
        }
        
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f)
        
        messagebox.showinfo("Success", "Registration Successful!")
        registration_window.destroy()
    
    # Creating the registration window
    registration_window = tk.Toplevel(app)
    registration_window.title("Registration Form")
    registration_window.geometry("400x400")
    registration_window.configure(bg="#1d314d")

    # Registration Form Widgets
    tk.Label(registration_window, text="Name", bg="#6b5717", fg="white").pack(pady=5)
    name_entry = tk.Entry(registration_window)
    name_entry.pack(pady=5)

    tk.Label(registration_window, text="Date of Birth", bg="#6b5717", fg="white").pack(pady=5)
    dob_entry = tk.Entry(registration_window)
    dob_entry.pack(pady=5)

    tk.Label(registration_window, text="Country", bg="#6b5717", fg="white").pack(pady=5)
    country_entry = tk.Entry(registration_window)
    country_entry.pack(pady=5)

    tk.Label(registration_window, text="City", bg="#6b5717", fg="white").pack(pady=5)
    city_entry = tk.Entry(registration_window)
    city_entry.pack(pady=5)

    tk.Label(registration_window, text="Gender", bg="#6b5717", fg="white").pack(pady=5)
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(registration_window, text="Male", variable=gender_var, value="Male", bg="#6b5717", fg="white").pack(pady=5)
    tk.Radiobutton(registration_window, text="Female", variable=gender_var, value="Female", bg="#6b5717", fg="white").pack(pady=5)

    tk.Label(registration_window, text="Username", bg="#6b5717", fg="white").pack(pady=5)
    username_entry = tk.Entry(registration_window)
    username_entry.pack(pady=5)

    tk.Label(registration_window, text="Password", bg="#6b5717", fg="white").pack(pady=5)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(registration_window, text="Register", command=save_details, bg="#6b5717", fg="white").pack(pady=20)

# Function to login user
def login_user():
    def authenticate():
        if not os.path.exists('user_data.json'):
            messagebox.showerror("Error", "No users registered. Please register first.")
            return
        
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
        
        if username_entry.get() == user_data['username'] and password_entry.get() == user_data['password']:
            messagebox.showinfo("Success", "Login Successful!")
            login_window.destroy()
            open_user_details(user_data)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # Creating the login window
    login_window = tk.Toplevel(app)
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.configure(bg="#1d314d")

    tk.Label(login_window, text="Username", bg="#6b5717", fg="white").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password", bg="#6b5717", fg="white").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    

    tk.Label(app, text="Login", command=authenticate, bg="6b5717", fg="white").pack(pady=20)

# Function to display user details after login
def open_user_details(user_data):
    details_window = tk.Toplevel(app)
    details_window.title("User Details")
    details_window.geometry("400x400")
    details_window.configure(bg="6b5717")

    tk.Label(details_window, text="User Details", font=("Arial", 18), bg="#d4af37", fg="white").pack(pady=10)

    for key, value in user_data.items():
        tk.Label(details_window, text=f"{key.capitalize()}: {value}", bg="#d4af37", fg="white").pack(pady=5)

# Function to update the background image on window resize
def resize_bg(event):
    new_width = event.width
    new_height = event.height
    resized_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_image)
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection

# Main application window
app = tk.Tk()
app.title("Job Application App")
app.geometry("600x400")  # Set initial window size

# Load the background image
bg_image = Image.open("/home/dci-students/Desktop/Working-Working-API/Nessa/istockphoto-1270389718-612x612.jpg")

# Create a label for the background image
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bind the resize event to the resize_bg function
app.bind("<Configure>", resize_bg)

# Main window buttons
register_button = tk.Button(app, text="Register", command=register_user, bg="#6b5717", fg="white", width=20, height=2)
register_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

login_button = tk.Button(app, text="Login", command=login_user, bg="#6b5717", fg="white", width=20, height=2)
login_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

app.mainloop()
