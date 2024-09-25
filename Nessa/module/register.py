import tkinter as tk
from tkinter import messagebox, END
import customtkinter as ctk
import json
import psycopg2

# Database configuration
DB_NAME = "k47a"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"

# Set CustomTkinter settings
ctk.set_appearance_mode("dark")  # Default mode
ctk.set_default_color_theme("Nessa/CTK_THEMES/blue.json")

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to toggle between light and dark modes
mode = "dark"

def toggle_mode():
    global mode
    if mode == "dark":
        ctk.set_appearance_mode("light")
        mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        mode = "dark"

# Registration form for user data collection
def open_register():
    """Opens the registration window."""
    register_window = ctk.CTk()
    register_window.title("Register")

    window_width = 600
    window_height = 600
    center_window(register_window, window_width, window_height)

    def save_details():
        """Save the registration details to a local JSON file."""
        user_data = {
            "name": name_entry.get(),
            "dob": dob_entry.get(),
            "country": country_entry.get(),
            "city": city_entry.get(),
            "gender": gender_var.get(),
            "email": email_entry.get(),  # Collect email
            "username": username_entry.get(),
            "password": password_entry.get()
        }

        # Save data to JSON
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f)

        messagebox.showinfo("Success", "Registration Successful!")
        register_window.destroy()

    def register_user():
        """Registers the user into the database."""
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()  # Collect email for database

        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)
            )
            conn.commit()

            messagebox.showinfo("Success", "User registered successfully")
            register_window.destroy()

            cur.close()
            conn.close()

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Registration Form Widgets
    ctk.CTkLabel(register_window, text="Register Form", font=("Arial", 20)).grid(row=0, columnspan=2, pady=20, sticky="e")

    ctk.CTkLabel(register_window, text="Name").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    name_entry = ctk.CTkEntry(register_window)
    name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="Date of Birth").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    dob_entry = ctk.CTkEntry(register_window)
    dob_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="Country").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    country_entry = ctk.CTkEntry(register_window)
    country_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="City").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    city_entry = ctk.CTkEntry(register_window)
    city_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="Gender").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    gender_var = tk.StringVar(value="Male")
    ctk.CTkRadioButton(register_window, text="Male", variable=gender_var, value="Male").grid(row=5, column=1, padx=10, pady=5, sticky="e")
    ctk.CTkRadioButton(register_window, text="Female", variable=gender_var, value="Female").grid(row=5, column=2, padx=10, pady=5, sticky="e")

    ctk.CTkLabel(register_window, text="Email").grid(row=6, column=0, padx=10, pady=10, sticky="e")
    email_entry = ctk.CTkEntry(register_window)
    email_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="Username").grid(row=7, column=0, padx=10, pady=10, sticky="e")
    username_entry = ctk.CTkEntry(register_window)
    username_entry.grid(row=7, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkLabel(register_window, text="Password").grid(row=8, column=0, padx=10, pady=10, sticky="e")
    password_entry = ctk.CTkEntry(register_window, show="*")  # Ensure the 'show' parameter is set correctly for password masking
    password_entry.grid(row=8, column=1, padx=10, pady=10, sticky="e")

    # Button frame to hold buttons in a row
    button_frame = ctk.CTkFrame(register_window)
    button_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

    # Button to save details locally (left-aligned)
    register_local_button = ctk.CTkButton(button_frame, text="Save Locally", command=save_details)
    register_local_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Button to register into the database (centered)
    register_db_button = ctk.CTkButton(button_frame, text="Register to Database", command=register_user)
    register_db_button.grid(row=0, column=1, padx=10, pady=10)

    # Button to toggle between light/dark mode (right-aligned)
    toggle_mode_button = ctk.CTkButton(button_frame, text="Toggle Light/Dark", command=toggle_mode)
    toggle_mode_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Configure columns to stretch the buttons appropriately
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    register_window.mainloop()

# Initialize the registration window
open_register()
