import customtkinter as ctk
from tkinter import messagebox, filedialog, Menu
import psycopg2
import json
import os
#from openai import OpenAI
from faker import Faker
import requests
from PIL import Image, ImageTk
import requests
import tkinter as tk
import tkinter.filedialog as filedialog
#import ApplicationTrackerApp




# Database connection setup
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=" postgres",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
        return None


# Function to create the database and tables if they don't exist
def create_database_and_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            dob DATE,
            country VARCHAR(100),
            city VARCHAR(100),
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        );
        ''')
        conn.commit()
        cursor.close()
        conn.close()


    # Registration window form
    
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
    

    #   # Creating the registration window
    registration_window = tk.Toplevel(app)
    registration_window.title("Registration Form")
    registration_window.geometry("400x400")
    registration_window.configure(bg="#1d314d")

    # Registration Form Widgets arranged in a grid
    tk.Label(registration_window, text="Name", bg="#6b5717", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(registration_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Date of Birth", bg="#6b5717", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    dob_entry = tk.Entry(registration_window)
    dob_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Country", bg="#6b5717", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    country_entry = tk.Entry(registration_window)
    country_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="City", bg="#6b5717", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    city_entry = tk.Entry(registration_window)
    city_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Gender", bg="#6b5717", fg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(registration_window, text="Male", variable=gender_var, value="Male", bg="#6b5717", fg="white").grid(row=4, column=1, padx=10, pady=5, sticky="w")
    tk.Radiobutton(registration_window, text="Female", variable=gender_var, value="Female", bg="#6b5717", fg="white").grid(row=4, column=2, padx=10, pady=5, sticky="w")

    tk.Label(registration_window, text="Username", bg="#6b5717", fg="white").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Password", bg="#6b5717", fg="white").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=6, column=1, padx=10, pady=5)

    # Register button spans across columns
    tk.Button(registration_window, text="Register", command=save_details, bg="#6b5717", fg="white").grid(row=7, columnspan=2, pady=20)

# Function to login user
def login_user():
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                # Validate user credentials
                cur.execute("""
                    SELECT * FROM users WHERE username = %s AND password = %s
                """, (username, password))
                user = cur.fetchone()
                if user:
                    messagebox.showinfo("Success", "Login Successful!")
                    login_window.destroy()
                    open_user_dashboard(user)
                else:
                    messagebox.showerror("Error", "Invalid Username or Password")
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {e}")
            finally:
                cur.close()
                conn.close()

    # Creating the app  window
    login_window = ctk.CTkToplevel(app)
    login_window.title("Application Tracker")
    login_window.geometry("600x300")
    login_window.configure(bg="#1d314d")

   # ctk.CTkLabel(login_window, text="Username", text_color="white").pack(pady=10)
   # username_entry = ctk.CTkEntry(login_window)
   # username_entry.pack(pady=5)

    #ctk.CTkLabel(login_window, text="Password", text_color="white").pack(pady=10)
    #password_entry = ctk.CTkEntry(login_window, show="*")
    #
    #ctk.CTkButton(login_window, text="Login", command=authenticate, fg_color="#6b5717").pack(pady=20)


    def login_user(self):
        # Implement your login logic here, check username and password against a database or other mechanism
        # If login is successful, call open_job_tracker()

        username = self.username_var.get()
        password = self.password_var.get()

        # (Replace with your actual login validation logic)
        if username == "test_user" and password == "test_password":
            self.open_job_tracker()
        else:
            # Show a login failed message
            pass

 # Open the Application Tracker in a new window
    def open_job_tracker(self):
        job_tracker_window.geometry("1200x800")
        job_tracker_window = tk.Toplevel(self)
        job_tracker_window.title("Job Tracker")
        job_tracker_window.geometry("1200x800")

        # Instantiate the ApplicationTrackerApp in the new window
        app = ApplicationTrackerApp(job_tracker_window)
        app.pack(fill="both", expand=True)
    
    def register_user(self):
        # Registration logic goes here
        pass


# Function to open user dashboard
def open_user_dashboard(user_data):
    dashboard_window = ctk.CTkToplevel(app)
    dashboard_window.title("User Dashboard")
    dashboard_window.geometry("600x400")
    dashboard_window.configure(bg="#1d314d")

    ctk.CTkLabel(dashboard_window, text=f"Welcome, {user_data[1]}", text_color="white").place(x=10, y=10)

    # Search box for job URLs
    search_frame = ctk.CTkFrame(dashboard_window, fg_color="#6b5717")
    search_frame.pack(pady=20, padx=20, fill="x")

    search_label = ctk.CTkLabel(search_frame, text="Enter Job URL:", text_color="white")
    search_label.pack(side="left", padx=5)

    search_entry = ctk.CTkEntry(search_frame, width=400)
    search_entry.pack(side="left", padx=5)

    # User Options
    ctk.CTkButton(dashboard_window, text="Log Out", command=dashboard_window.destroy, fg_color="#6b5717").place(x=450, y=240)


# Main application window
app = ctk.CTk()
app.title("Job Tracker")
app.geometry("600x400")

# Load and set the background image
def create_background_image(app, image_path):
    image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(image)

    bg_label = tk.Label(app, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection

# Use your background image path
create_background_image(app, "/home/dci-students/Desktop/Working-Working-API/Nessa/istockphoto-1270389718-612x612.jpg")

# Main window widgets (Login and Registration)
ctk.CTkLabel(app, text="Username", text_color="white").place(x=220, y=150)
username_entry = ctk.CTkEntry(app)
username_entry.place(x=300, y=150)

ctk.CTkLabel(app, text="Password", text_color="white").place(x=220, y=180)
password_entry = ctk.CTkEntry(app, show="*")
password_entry.place(x=300, y=180)

ctk.CTkButton(app, text="Login", command=login_user, fg_color="#6b5717").place(x=300, y=220)
ctk.CTkButton(app, text="Register", command=register_user, fg_color="#6b5717").place(x=300, y=270)

app.mainloop()


