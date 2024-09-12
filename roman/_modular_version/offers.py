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

def scrape_offer(user_id, url_entry, root):
    """Scrapes offer data from a given URL and saves it to the offers table."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    try:
        from scrape_module.scraper import get_offer_information  # Import the scraper function

        # Call the scraping function and get offer data
        offer_information = get_offer_information(url)

        if not offer_information or len(offer_information) < 4:
            messagebox.showerror("Error", "Failed to scrape offer information. Please check the URL or scraper.")
            return

        # Unpack the offer information
        company = offer_information[0]
        position = offer_information[1]
        about = offer_information[2]
        offer_list = offer_information[3]

        if not isinstance(offer_list, list):
            messagebox.showerror("Error", "Offer information is not in the expected format.")
            return

        offer_text = ' '.join(offer_list)  # Concatenate list of strings

        # Save the offer data into the offers table
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO offers (position, company, offer, about, url, status, response, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (position, company, offer_text, about, url, 0, False, user_id))

        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Success", "Offer scraped and saved successfully!")
        root.destroy()  # Close the current window
        open_offers(user_id)  # Open the refreshed offers window

    except ImportError as e:
        messagebox.showerror("Import Error", f"Error importing scraper: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_offers(user_id):
    """Opens the window displaying the user's offers."""
    root = tk.Tk()
    root.title("Your Offers")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    # Fetch the offers for the logged-in user
    offers = fetch_offers(user_id)

    # Frame for the offers list
    offers_frame = tk.Frame(root)
    offers_frame.pack(pady=10)

    # Labels for the columns
    tk.Label(offers_frame, text="Position", width=20, anchor="w").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(offers_frame, text="Company", width=20, anchor="w").grid(row=0, column=1, padx=10, pady=10)
    tk.Label(offers_frame, text="Action", width=10).grid(row=0, column=2, padx=10, pady=10)

    # Display each offer with a "Select" button
    for idx, offer in enumerate(offers):
        offer_id, position, company, status, response = offer
        tk.Label(offers_frame, text=position, width=20, anchor="w").grid(row=idx+1, column=0, padx=10, pady=5)
        tk.Label(offers_frame, text=company, width=20, anchor="w").grid(row=idx+1, column=1, padx=10, pady=5)

        # Button to select and view offer details
        select_button = tk.Button(offers_frame, text="Select", command=lambda offer_id=offer_id: (root.destroy(), open_offer_details(offer_id, user_id)))
        select_button.grid(row=idx+1, column=2, padx=10, pady=5)

    # Back button to return to the menu
    back_button = tk.Button(root, text="Back", command=lambda: (root.destroy(), open_menu(user_id)))
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    # New Offer button to open the new offer form
    new_offer_button = tk.Button(root, text="New Offer", command=lambda: (root.destroy(), open_new_offer(user_id)))
    new_offer_button.pack(side=tk.LEFT, padx=10, pady=10)

    # URL input field and button to scrape an offer
    tk.Label(root, text="Enter URL to scrape offer:", anchor="w").pack(pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    scrape_button = tk.Button(root, text="Scrape Offer from URL", command=lambda: scrape_offer(user_id, url_entry, root))
    scrape_button.pack(pady=5)

    root.mainloop()
