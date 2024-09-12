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
        # Get the form details
        user_data = {
            "first_name": first_name_entry.get(),
            "last_name": last_name_entry.get(),
            "dob": dob_entry.get(),
            "country": country_entry.get(),
            "city": city_entry.get(),
            "username": username_entry.get(),
            "password": password_entry.get()
        }

        # Save user data to the PostgreSQL database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO users (first_name, last_name, dob, country, city, username, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_data["first_name"],
                    user_data["last_name"],
                    user_data["dob"],
                    user_data["country"],
                    user_data["city"],
                    user_data["username"],
                    user_data["password"]
                ))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful!")
                registration_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                cur.close()
                conn.close()

    # Creating the registration window
    registration_window = ctk.CTkToplevel(app)
    registration_window.title("Registration Form")
    registration_window.geometry("400x400")
    registration_window.configure(bg="#1d314d")

    # Registration Form Widgets
    tk.Label(registration_window, text="First Name", bg="#6b5717", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    first_name_entry = tk.Entry(registration_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Last Name", bg="#6b5717", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    last_name_entry = tk.Entry(registration_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Date of Birth", bg="#6b5717", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    dob_entry = tk.Entry(registration_window)
    dob_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Country", bg="#6b5717", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    country_entry = tk.Entry(registration_window)
    country_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="City", bg="#6b5717", fg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    city_entry = tk.Entry(registration_window)
    city_entry.grid(row=4, column=1, padx=10, pady=5)


    tk.Label(registration_window, text="Username", bg="#6b5717", fg="white").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(registration_window, text="Password", bg="#6b5717", fg="white").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=6, column=1, padx=10, pady=5)

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
    

# Function to open the home page after login
def open_home_page(user_data):
    #test()
    #home_page = ctk.CTkToplevel(app)
    #home_page.title("Home Page - Application Tracker")
    #home_page.geometry("1200x800")

    # Add content to the home page (e.g., header, buttons)
    #ctk.CTkLabel(home_page, text=f"Welcome {user_data[1]}!", text_color="white", font=("Roboto", 24)).pack(pady=20)
    
    # Insert the home page widgets here as per your original design
    # For example:
    #ctk.CTkLabel(home_page, text="This is the Home Page", text_color="white", font=("Roboto", 18)).pack(pady=20)
  pass
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


def center_widget(widget, widget_width, y_position):
    # Get the width of the window
    window_width = app.winfo_width()
    # Calculate x position to center the widget
    x_position = (window_width - widget_width) // 2
    widget.place(x=x_position, y=y_position)


# Main window widgets
ctk.CTkLabel(app, text="Bravo Application Tracker", text_color="white", font=("Roboto", 20)).place(x=200, y=50)

# Create the buttons without placing them initially
login_button = ctk.CTkButton(app, text="Login", command=login_user, fg_color="#6b5717")
register_button = ctk.CTkButton(app, text="Register", command=register_user, fg_color="#6b5717")

# Center the buttons by calling the helper function
app.update()  # Update the app to get the correct window size

center_widget(login_button, login_button.winfo_reqwidth(), 320)
center_widget(register_button, register_button.winfo_reqwidth(), 270)


create_database_and_tables()  # Ensure tables exist

app.mainloop()
