import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt

DB_NAME = "job_app_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def create_db_and_tables():
    """Creates necessary database tables if they do not exist."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS p_info (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                background TEXT,
                user_id INTEGER REFERENCES users(id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                position VARCHAR(100) NOT NULL,
                company VARCHAR(100) NOT NULL,
                offer TEXT,
                about TEXT,
                url VARCHAR(255),
                status INTEGER,
                response BOOLEAN,
                user_id INTEGER REFERENCES users(id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                resume TEXT,
                user_id INTEGER REFERENCES users(id),
                offer_id INTEGER REFERENCES offers(id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database tables: {e}")

def login():
    """Handles login action."""
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in both fields")
        return

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("SELECT id, password FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user:
            user_id, stored_hashed_password = user

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                messagebox.showinfo("Success", "Login successful")
                root.withdraw()  # Hide login window
                from menu import open_menu  # Import here to avoid circular import
                open_menu(user_id)  # Call the menu module after login
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            messagebox.showerror("Error", "User not found")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_register_window():
    """Opens the registration window."""
    root.withdraw()  # Hide the login window
    from register import open_register  # Import here to avoid circular import
    open_register()

def on_enter_key(event):
    login()

def open_login():
    """Opens the login window."""
    global username_entry, password_entry, root

    root = tk.Tk()
    root.title("Login")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(root, text="Login", command=login)
    login_button.grid(row=2, column=1, padx=10, pady=10)

    register_button = tk.Button(root, text="Register", command=open_register_window)
    register_button.grid(row=3, column=1, padx=10, pady=10)

    root.bind('<Return>', on_enter_key)

    root.mainloop()

if __name__ == "__main__":
    create_db_and_tables()
    open_login()
