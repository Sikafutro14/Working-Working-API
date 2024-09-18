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

    idx = 0
    
    """Opens the window displaying the user's offers."""
    root = tk.Tk()
    root.title("Your Offers")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    # Fetch the offers for the logged-in user
    offers = fetch_offers(user_id)

    # Frame for the offers list and buttons
    offers_frame = tk.Frame(root)
    offers_frame.pack(pady=10)

    # Labels for the columns
    tk.Label(offers_frame, text="Position", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    tk.Label(offers_frame, text="Company", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=10, columnspan=2)
    tk.Label(offers_frame, text="Action", width=10, font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10, pady=10)

    # Function to return the color based on offer status
    def get_status_color(status):
        """Returns a lighter color based on the offer status."""
        if status == 3:  # Rejected
            return 'red'  # Light red
        elif status == 4:  # Accepted
            return 'green'  # Light green
        elif status == 1:  # Open
            return 'yellow'  # Light yellow
        elif status == 2:  # Applied
            return 'lightblue'  # Magenta (instead of dark blue)
        return 'white'  # Default for "None" or unknown statuses

    # Display each offer with a "Select" button and background colors for status
    for idx, offer in enumerate(offers):
        offer_id, position, company, status, response = offer
        status_color = get_status_color(status)  # Get color for the current status

        # Display position, company, with background color and no color for the button
        position_label = tk.Label(offers_frame, text=position, width=20, anchor="w", bg=status_color)
        position_label.grid(row=idx+2, column=0, padx=10, pady=5, columnspan=2)

        company_label = tk.Label(offers_frame, text=company, width=20, anchor="w", bg=status_color)
        company_label.grid(row=idx+2, column=2, padx=10, pady=5, columnspan=2)

        select_button = tk.Button(offers_frame, text="Select", command=lambda offer_id=offer_id: (root.destroy(), open_offer_details(offer_id, user_id)))
        select_button.grid(row=idx+2, column=4, padx=10, pady=5)

    # Line under Offers

    # idx = 0

    tk.Label(offers_frame, text="-------------------", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=idx+3, column=0, padx=10, pady=10, columnspan=2)
    tk.Label(offers_frame, text="-------------------", width=20, anchor="w", font=("Arial", 10, "bold")).grid(row=idx+3, column=2, padx=10, pady=10, columnspan=2)
    tk.Label(offers_frame, text="-------------------", width=10, font=("Arial", 10, "bold")).grid(row=idx+3, column=4, padx=10, pady=10)

    # URL input field and button to scrape an offer (placed below the offers list)
    tk.Label(offers_frame, text="Enter URL to scrape offer:", anchor="w").grid(row=idx+4, column=0, padx=10, pady=5, columnspan=2, sticky="w")
    url_entry = tk.Entry(offers_frame, width=50)
    url_entry.grid(row=idx+4, column=2, padx=10, pady=5, columnspan=3)

    scrape_button = tk.Button(offers_frame, text="Scrape Offer from URL", command=lambda: scrape_offer(user_id, url_entry, root))
    scrape_button.grid(row=idx+6, column=4, padx=10, pady=5)

    # Back button to return to the menu (aligned with New Offer button)
    back_button = tk.Button(offers_frame, text="Back", command=lambda: (root.destroy(), open_menu(user_id)))
    back_button.grid(row=idx+6, column=0, padx=10, pady=10, sticky="e")

    # New Offer button to open the new offer form (aligned with Back button)
    new_offer_button = tk.Button(offers_frame, text="New Offer", command=lambda: (root.destroy(), open_new_offer(user_id)))
    new_offer_button.grid(row=idx+6, column=2, padx=10, pady=10, sticky="w")

    # Add a color-coded legend below the list
    legend_frame = tk.Frame(root)
    legend_frame.pack(pady=10)

    tk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
    tk.Label(legend_frame, text="Rejected", bg="red", width=10).grid(row=0, column=1, padx=10)
    tk.Label(legend_frame, text="Accepted", bg="green", width=10).grid(row=0, column=2, padx=10)
    tk.Label(legend_frame, text="Open", bg="yellow", width=10).grid(row=0, column=3, padx=10)
    tk.Label(legend_frame, text="Applied", bg="lightblue", width=10).grid(row=0, column=4, padx=10)

    root.mainloop()
