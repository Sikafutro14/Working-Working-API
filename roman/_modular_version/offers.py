import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection parameters
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

def fetch_offers(user_id):
    """Fetches the list of offers for the given user from the database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Fetch the offers for the logged-in user
        cur.execute("SELECT id, position, company, status, response FROM offers WHERE user_id = %s", (user_id,))
        offers = cur.fetchall()

        cur.close()
        conn.close()

        return offers
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching offers: {e}")
        return []

def open_offer_details(offer_id, user_id):
    import offer  # Make sure the offer module is correctly imported
    offer.open_offer(offer_id, user_id)  # Pass both offer_id and user_id to open_offer


def open_new_offer(user_id):
    """Opens the window to add a new offer (new_offer.py)."""
    import new_offer  # Assuming new_offer.py contains the form to create a new offer
    new_offer.open_new_offer(user_id)

def open_menu(user_id):
    """Returns to the main menu (menu.py)."""
    import menu  # Assuming menu.py contains the main menu logic
    menu.open_menu(user_id)

def open_offers(user_id):
    """Opens the window displaying the user's offers."""
    offers_window = tk.Toplevel()
    offers_window.title("Your Offers")

    window_width = 1024
    window_height = 768

    center_window(offers_window, window_width, window_height)

    # Fetch the offers for the logged-in user
    offers = fetch_offers(user_id)

    # Labels for the columns
    tk.Label(offers_window, text="Position", width=20, anchor="w").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(offers_window, text="Company", width=20, anchor="w").grid(row=0, column=1, padx=10, pady=10)
    tk.Label(offers_window, text="Status", width=15, anchor="w").grid(row=0, column=2, padx=10, pady=10)
    tk.Label(offers_window, text="Response", width=15, anchor="w").grid(row=0, column=3, padx=10, pady=10)
    tk.Label(offers_window, text="Action", width=10).grid(row=0, column=4, padx=10, pady=10)

    # Display each offer with a "Select" button
    for idx, offer in enumerate(offers):
        offer_id, position, company, status, response = offer
        tk.Label(offers_window, text=position, width=20, anchor="w").grid(row=idx+1, column=0, padx=10, pady=5)
        tk.Label(offers_window, text=company, width=20, anchor="w").grid(row=idx+1, column=1, padx=10, pady=5)
        tk.Label(offers_window, text=status, width=15, anchor="w").grid(row=idx+1, column=2, padx=10, pady=5)
        tk.Label(offers_window, text=response, width=15, anchor="w").grid(row=idx+1, column=3, padx=10, pady=5)

        # Button to select and view offer details
        select_button = tk.Button(offers_window, text="Select", command=lambda offer_id=offer_id: open_offer_details(offer_id, user_id))

        select_button.grid(row=idx+1, column=4, padx=10, pady=5)

    # Back button to return to the menu
    back_button = tk.Button(offers_window, text="Back", command=lambda: (offers_window.destroy(), open_menu(user_id)))
    back_button.grid(row=len(offers)+1, column=0, padx=10, pady=10)

    # New Offer button to open the new offer form
    new_offer_button = tk.Button(offers_window, text="New Offer", command=lambda: open_new_offer(user_id))
    new_offer_button.grid(row=len(offers)+1, column=1, padx=10, pady=10)

    offers_window.mainloop()
