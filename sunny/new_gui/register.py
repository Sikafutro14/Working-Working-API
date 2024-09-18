import customtkinter as ctk
import psycopg2
import bcrypt

# Database connection parameters (assuming defined elsewhere)
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


def hash_password(password):
    """Hashes the password using bcrypt and returns it as a string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Store as a UTF-8 string


def check_password(stored_password, provided_password):
    """Checks if the provided password matches the stored hashed password."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


def open_login_window():
    """Closes the register window and reopens the login window."""
    import main
    print("Opening login window")
    main.open_login()  # Assuming this function exists in main.py


def register_user():
    """Registers the user and then opens the login window."""
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not username or not email or not password:
        ctk.CTkMessageBox.showerror("Error", "Please fill in all fields")
        return

    try:
        hashed_password = hash_password(password)

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()

        ctk.CTkMessageBox.showinfo("Success", "User registered successfully")
        register_window.destroy()
        open_login_window()

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        ctk.CTkMessageBox.showerror("Database Error", f"An error occurred while connecting to the database: {e}")
    except Exception as e:
        ctk.CTkMessageBox.showerror("Error", f"An unexpected error occurred: {e}")


def open_register():
    """Opens the registration window."""
    register_window = ctk.CTk()
    register_window.title("Register")

    window_width = 1024
    window_height = 768

    center_window(register_window, window_width, window_height)

    def on_enter_key(event):
        register_user()

    username_label = ctk.CTkLabel(register_window, text="Username")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    username_entry = ctk.CTkEntry(register_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    email_label = ctk.CTkLabel(register_window, text="Email")
    email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    email_entry = ctk.CTkEntry(register_window)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = ctk.CTkLabel(register_window, text="Password")
    password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    password_entry = ctk.CTkEntry(register_window, show='*')
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    register_button = ctk.CTkButton(register_window, text="Register", command=register_user)
    register_button.grid(row=3, column=1, padx=10, pady=10)

    back_button = ctk.CTkButton(register_window, text="Back", command=open_login_window)
    back_button.grid(row=4, column=1, padx=10, pady=10)

    register_window.bind('<Return>', on_enter_key)

    username_entry.focus_set()
    username_entry.bind("<Tab>", lambda e: email_entry.focus_set())
    email_entry.bind("<Tab>", lambda e: password_entry.focus_set())
    password_entry.bind("<Tab>", lambda e: register_button.focus_set())

    register_window.mainloop()