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

def save_offer(user_id, position, company, offer_text, about_company, url):
    """Saves the offer details into the database."""
    if not position or not company or not offer_text or not about_company or not url:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Insert the offer into the offers table
        cur.execute(
            "INSERT INTO offers (user_id, position, company, offer, about, url) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, position, company, offer_text, about_company, url)
        )
        conn.commit()

        messagebox.showinfo("Success", "Offer saved successfully")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving the offer: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def open_offers_window(user_id):
    """Returns to the offers window (offers.py)."""
    import offers  # Assuming offers.py has the function to display the offers list
    offers.open_offers(user_id)

def open_new_offer(user_id):
    """Opens the window to create a new offer."""
    root = tk.Tk()
    root.title("New Offer")

    window_width = 1024
    window_height = 768
    
    center_window(root, window_width, window_height)

    # Input fields for the offer details
    tk.Label(root, text="Position").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    position_entry = tk.Entry(root, width=50)
    position_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Company").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    company_entry = tk.Entry(root, width=50)
    company_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Offer").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    offer_text = tk.Text(root, width=50, height=5)
    offer_text.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="About the Company").grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    about_company_text = tk.Text(root, width=50, height=5)
    about_company_text.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="URL").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=4, column=1, padx=10, pady=10)

    def save():
        """Handles the save button click event."""
        position = position_entry.get()
        company = company_entry.get()
        offer = offer_text.get("1.0", tk.END).strip()
        about_company = about_company_text.get("1.0", tk.END).strip()
        url = url_entry.get()
        save_offer(user_id, position, company, offer, about_company, url)

    # Save button
    save_button = tk.Button(root, text="Save", command=save)
    save_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")

    # Back button to go back to the offers list
    back_button = tk.Button(root, text="Back", command=lambda: (root.destroy(), open_offers_window(user_id)))
    back_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    root.mainloop()
