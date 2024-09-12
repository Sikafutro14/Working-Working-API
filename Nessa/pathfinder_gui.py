import customtkinter as ctk
from tkinter import messagebox
import psycopg2
import json
import requests
from PIL import Image, ImageTk
import tkinter as tk

# Database connection setup
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
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

# Function to register user details
def register_user():
    def save_details():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        dob = dob_entry.get()
        country = country_entry.get()
        city = city_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO users (first_name, last_name, dob, country, city, username, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, dob, country, city, username, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful!")
                registration_window.destroy()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                cur.close()
                conn.close()

    registration_window = tk.Toplevel(app)
    registration_window.title("Registration Form")
    registration_window.geometry("400x400")

    tk.Label(registration_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = tk.Entry(registration_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = tk.Entry(registration_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Date of Birth").grid(row=2, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(registration_window)
    dob_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Country").grid(row=3, column=0, padx=10, pady=5)
    country_entry = tk.Entry(registration_window)
    country_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="City").grid(row=4, column=0, padx=10, pady=5)
    city_entry = tk.Entry(registration_window)
    city_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Username").grid(row=5, column=0, padx=10, pady=5)
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Password").grid(row=6, column=0, padx=10, pady=5)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Button(registration_window, text="Register", command=save_details).grid(row=7, columnspan=2, pady=10)

# Function to login user
def login_user():
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
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

    login_window = tk.Toplevel(app)
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=authenticate).pack(pady=20)

def open_user_dashboard(user_data):
    dashboard_window = tk.Toplevel(app)
    dashboard_window.title("User Dashboard")
    dashboard_window.geometry("600x400")

    tk.Label(dashboard_window, text=f"Welcome, {user_data[1]}").pack(pady=10)

    search_frame = tk.Frame(dashboard_window)
    search_frame.pack(pady=20)

    tk.Label(search_frame, text="Enter Job URL:").pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side="left", padx=5)

    def fetch_job_details():
        job_url = search_entry.get()
        try:
            response = requests.get(job_url)
            if response.status_code == 200:
                job_data = response.text
                messagebox.showinfo("Job Details", job_data)
            else:
                messagebox.showerror("Error", "Failed to fetch job details")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch details: {e}")

    tk.Button(search_frame, text="Search", command=fetch_job_details).pack(side="left", padx=5)

    tk.Button(dashboard_window, text="Log Out", command=dashboard_window.destroy).pack(pady=20)

# Main application window
app = ctk.CTk()
app.title("Job Tracker")
app.geometry("600x400")

def create_background_image(app, image_path):
    image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(app, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection

# Use your background image path
create_background_image(app, "/home/dci-students/Desktop/Working-Working-API/Nessa/istockphoto-1270389718-612x612.jpg")

# Main window widgets
tk.Label(app, text="Username").place(x=220, y=150)
username_entry = tk.Entry(app)
username_entry.place(x=300, y=150)

tk.Label(app, text="Password").place(x=220, y=180)
password_entry = tk.Entry(app, show="*")
password_entry.place(x=300, y=180)

tk.Button(app, text="Login", command=login_user).place(x=300, y=220)
tk.Button(app, text="Register", command=register_user).place(x=300, y=270)

app.mainloop()
