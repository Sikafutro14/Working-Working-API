import customtkinter as ctk
from tkinter import messagebox
import psycopg2
import json
from PIL import Image, ImageTk
import tkinter as tk
from Job_Traker_HomeP import test

# Database connection setup
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="ApplicationTrackerApp",
            user="postgres",  # Replace with your actual PostgreSQL username
            password="password",  # Replace with your actual PostgreSQL password
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
        # Create the necessary tables for user info and resume data
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
        CREATE TABLE IF NOT EXISTS user_resume_info (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            full_name VARCHAR(100),
            email VARCHAR(100),
            phone_number VARCHAR(20),
            location VARCHAR(100),
            objective TEXT,
            work_experience JSONB,
            education JSONB,
            skills TEXT,
            achievements TEXT,
            volunteer_work TEXT,
            references JSONB
        );
        ''')
        conn.commit()
        cursor.close()
        conn.close()

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
                    open_home_page(user)
                    test()
                else:
                    messagebox.showerror("Error", "Invalid Username or Password")
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {e}")
            finally:
                cur.close()
                conn.close()

    # Creating the login window
    login_window = ctk.CTkToplevel(app)
    login_window.title("Job Tracker Login")
    login_window.geometry("600x300")
    login_window.configure(bg="#1d314d")

    ctk.CTkLabel(login_window, text="Username", text_color="white").place(x=220, y=150)
    username_entry = ctk.CTkEntry(login_window)
    username_entry.place(x=300, y=150)

    ctk.CTkLabel(login_window, text="Password", text_color="white").place(x=220, y=180)
    password_entry = ctk.CTkEntry(login_window, show="*")
    password_entry.place(x=300, y=180)

    ctk.CTkButton(login_window, text="Login", command=authenticate, fg_color="#6b5717").place(x=300, y=220)

# Main application window
app = ctk.CTk()
app.title("Application Tracker")
app.geometry("600x400")

# Load and set the background image (optional)
def create_background_image(app, image_path):
    image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(image)

    bg_label = tk.Label(app, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection

# Use your background image path if required
create_background_image(app, "/home/dci-students/Desktop/Working-Working-API/Nessa/istockphoto-1270389718-612x612.jpg")

# Main window widgets
ctk.CTkLabel(app, text="Bravo Application Tracker", text_color="white", font=("Roboto", 20)).place(x=200, y=50)

# Create the buttons
login_button = ctk.CTkButton(app, text="Login", command=login_user, fg_color="#6b5717")
register_button = ctk.CTkButton(app, text="Register", command=register_user, fg_color="#6b5717")
add_personal_info_button = ctk.CTkButton(app, text="Add Personal Info", command=add_personal_info, fg_color="#6b5717")

# Center the buttons
app.update()  # Update the app to get the correct window size
center_widget(login_button, login_button.winfo_reqwidth(), 320)
center_widget(register_button, register_button.winfo_reqwidth(), 270)
center_widget(add_personal_info_button, add_personal_info_button.winfo_reqwidth(), 370)

create_database_and_tables()  # Ensure tables exist
app.mainloop()
