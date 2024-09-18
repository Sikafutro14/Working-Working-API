import customtkinter as ctk
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_personal_data(user_id):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        # Example query to fetch personal data based on user_id
        cur.execute("SELECT * FROM personal_data WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        if rows:
            # Format the data as needed
            data = "\n".join([str(row) for row in rows])
            return data
        else:
            return "No personal data found for this user."

    except Exception as e:
        return f"Error: {str(e)}"

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


def load_user_data(user_id, first_name_entry, last_name_entry, email_entry, background_text):
    """Load the user's personal data from the database and populate the form."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("SELECT first_name, last_name, email, background FROM p_info WHERE user_id = %s", (user_id,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if data:
            first_name_entry.delete(0, ctk.END)
            first_name_entry.insert(0, data[0])
            last_name_entry.delete(0, ctk.END)
            last_name_entry.insert(0, data[1])
            email_entry.delete(0, ctk.END)
            email_entry.insert(0, data[2])
            background_text.delete(1.0, ctk.END)
            background_text.insert(ctk.END, data[3])
        else:
            ctk.CTkMessageBox.show_warning("Warning", "No data found for the user.")

    except psycopg2.Error as e:
        ctk.CTkMessageBox.show_error("Error", f"An error occurred while loading user data: {e}")


def save_user_data(user_id, first_name_entry, last_name_entry, email_entry, background_text):
    """Save the user's personal data to the database."""
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    background = background_text.get("1.0", ctk.END).strip()

    if not first_name or not last_name or not email:
        ctk.CTkMessageBox.show_error("Error", "Please fill in all required fields")
        return

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
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

        ctk.CTkMessageBox.show_info("Success", "Personal data saved successfully")
    except psycopg2.Error as e:
        ctk.CTkMessageBox.show_error("Error", f"An error occurred while saving user data: {e}")


def open_p_data(user_id):
    """Opens the personal data window."""
    p_data_window = ctk.CTk()
    p_data_window.title("Personal Data")

    # Define the window size
    window_width = 1024
    window_height = 768
    center_window(p_data_window, window_width, window_height)

    # Create labels and entry fields for personal data
    first_name_label = ctk.CTkLabel(p_data_window, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")
    first_name_entry = ctk.CTkEntry(p_data_window)
    first_name_entry.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    last_name_label = ctk.CTkLabel(p_data_window, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
    last_name_entry = ctk.CTkEntry(p_data_window)
    last_name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    email_label = ctk.CTkLabel(p_data_window, text="Email:")
    email_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
    email_entry = ctk.CTkEntry(p_data_window)
    email_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    background_label = ctk.CTkLabel(p_data_window, text="Background Info:")
    background_label.grid(row=3, column=0, padx=20, pady=10, sticky="ne")
    background_text = ctk.CTkTextbox(p_data_window, width=400, height=200)
    background_text.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    # Load data button
    load_button = ctk.CTkButton(p_data_window, text="Load Data", 
                                command=lambda: load_user_data(user_id, first_name_entry, last_name_entry, email_entry, background_text))
    load_button.grid(row=4, column=0, padx=20, pady=10, sticky="e")

    # Save data button
    save_button = ctk.CTkButton(p_data_window, text="Save Data", 
                                command=lambda: save_user_data(user_id, first_name_entry, last_name_entry, email_entry, background_text))
    save_button.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    # Close window button
    close_button = ctk.CTkButton(p_data_window, text="Close", command=p_data_window.destroy)
    close_button.grid(row=5, column=1, padx=20, pady=20, sticky="e")

    p_data_window.mainloop()
