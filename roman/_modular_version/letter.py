import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection parameters
DB_NAME = "ak47"
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

def save_letter(user_id, offer_id, letter_text):
    """Saves the modified letter text to the database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("""
            UPDATE applications
            SET resume = %s
            WHERE user_id = %s AND offer_id = %s
        """, (letter_text, user_id, offer_id))

        conn.commit()
        messagebox.showinfo("Success", "Letter saved successfully.")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving the letter: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def open_letter_window(user_id, offer_id):
    """Opens the letter window and displays the generated letter."""
    root = tk.Tk()
    root.title("Generated Letter")

    window_width = 1024
    window_height = 768
    center_window(root, window_width, window_height)

    # Fetch the generated letter from the database
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("SELECT resume FROM applications WHERE user_id = %s AND offer_id = %s", (user_id, offer_id))
        letter_data = cur.fetchone()

        if not letter_data:
            messagebox.showerror("Error", "No letter found for this offer.")
            root.destroy()
            return

        letter_text = letter_data[0]
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while retrieving the letter: {e}")
        root.destroy()
        return

    # Textbox for displaying and editing the letter
    text_box = tk.Text(root, wrap="word", width=100, height=30)
    text_box.insert("1.0", letter_text)
    text_box.grid(row=0, column=0, padx=10, pady=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, pady=20)

    save_button = tk.Button(button_frame, text="Save", command=lambda: save_letter(user_id, offer_id, text_box.get("1.0", tk.END).strip()))
    save_button.pack(side="left", padx=10)

    back_button = tk.Button(button_frame, text="Back", command=root.destroy)
    back_button.pack(side="left", padx=10)

    root.mainloop()
