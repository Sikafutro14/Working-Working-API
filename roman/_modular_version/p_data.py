import tkinter as tk
from tkinter import messagebox
import psycopg2

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

def load_user_data(user_id, root):
    """Load the user's personal data from the database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()
        cur.execute("SELECT first_name, last_name, email, background FROM p_info WHERE user_id = %s", (user_id,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        
        if data:
            first_name_entry.delete(0, tk.END)
            first_name_entry.insert(0, data[0])
            last_name_entry.delete(0, tk.END)
            last_name_entry.insert(0, data[1])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, data[2])
            background_entry.delete(1.0, tk.END)
            background_entry.insert(tk.END, data[3])
        else:
            messagebox.showwarning("Warning", "No data found for the user.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading user data: {e}")

def save_user_data(user_id):
    """Save the user's personal data to the database."""
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    background = background_entry.get(1.0, tk.END).strip()

    if not first_name or not last_name or not email:
        messagebox.showerror("Error", "Please fill in all required fields")
        return

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()

        # Check if the user already has a record in p_info
        cur.execute("SELECT COUNT(*) FROM p_info WHERE user_id = %s", (user_id,))
        record_exists = cur.fetchone()[0] > 0

        if record_exists:
            # Update existing record
            cur.execute("""
                UPDATE p_info 
                SET first_name = %s, last_name = %s, email = %s, background = %s
                WHERE user_id = %s
            """, (first_name, last_name, email, background, user_id))
        else:
            # Insert new record
            cur.execute("""
                INSERT INTO p_info (first_name, last_name, email, background, user_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, email, background, user_id))

        conn.commit()
        cur.close()
        conn.close()
        
        messagebox.showinfo("Success", "Personal data saved successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving user data: {e}")

def open_p_data(user_id):
    """Opens the personal data window."""
    p_data_window = tk.Tk()
    p_data_window.title("Personal Data")

    # Define the window size
    window_width = 1024
    window_height = 768

    # Center the window
    center_window(p_data_window, window_width, window_height)

    def on_save():
        save_user_data(user_id)

    def on_back():
        p_data_window.destroy()
        from menu import open_menu
        open_menu(user_id)

    # Personal data form fields
    tk.Label(p_data_window, text="First Name").grid(row=0, column=0, padx=10, pady=10)
    global first_name_entry
    first_name_entry = tk.Entry(p_data_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(p_data_window, text="Last Name").grid(row=1, column=0, padx=10, pady=10)
    global last_name_entry
    last_name_entry = tk.Entry(p_data_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(p_data_window, text="Email").grid(row=2, column=0, padx=10, pady=10)
    global email_entry
    email_entry = tk.Entry(p_data_window)
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(p_data_window, text="Background").grid(row=3, column=0, padx=10, pady=10)
    global background_entry
    background_entry = tk.Text(p_data_window, height=10, width=40)  # Larger text field for background
    background_entry.grid(row=3, column=1, padx=10, pady=10)

    # Save button
    save_button = tk.Button(p_data_window, text="Save", command=on_save)
    save_button.grid(row=4, column=1, padx=10, pady=10)

    # Back button
    back_button = tk.Button(p_data_window, text="Back", command=on_back)
    back_button.grid(row=5, column=1, padx=10, pady=10)

    # Set focus on the first entry when the window opens
    first_name_entry.focus_set()

    # Enable tabbing between input fields
    first_name_entry.bind("<Tab>", lambda e: last_name_entry.focus_set())
    last_name_entry.bind("<Tab>", lambda e: email_entry.focus_set())
    email_entry.bind("<Tab>", lambda e: background_entry.focus_set())
    background_entry.bind("<Tab>", lambda e: save_button.focus_set())

    # Load user data
    load_user_data(user_id, p_data_window)

    p_data_window.mainloop()
