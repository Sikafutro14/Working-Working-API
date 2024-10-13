import tkinter as tk
from tkinter import messagebox
import psycopg2
import offer  # Import to handle offer details
import new_offer  # Import to create a new offer
import menu  # Import to go back to menu
from scrape_module.scraper import get_offer_information  # Import for scraping functionality

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
        cur.execute("SELECT id, position, company, status, response FROM offers WHERE user_id = %s", (user_id,))
        offers = cur.fetchall()
        cur.close()
        conn.close()
        return offers
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching offers: {e}")
        return []

def delete_offer(offer_id, user_id):
    """Deletes the specified offer and its related data from the database."""
    confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this offer?")
    if not confirmation:
        return

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        # Delete related applications
        cur.execute("DELETE FROM applications WHERE offer_id = %s", (offer_id,))
        # Delete the offer from the offers table
        cur.execute("DELETE FROM offers WHERE id = %s", (offer_id,))
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Success", "Offer and related applications deleted successfully!")
        open_offers(user_id)  # Refresh the offers window after deletion

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while deleting the offer: {e}")

def open_offer_details(offer_id, user_id):
    offer.open_offer(offer_id, user_id)

def open_new_offer(user_id):
    new_offer.open_new_offer(user_id)

def open_menu(user_id):
    menu.open_menu(user_id)

def scrape_offer(user_id, url_entry, root):
    """Scrapes offer data from a given URL and saves it to the offers table."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    try:
        offer_information = get_offer_information(url)
        if not offer_information or len(offer_information) < 4:
            messagebox.showerror("Error", "Failed to scrape offer information. Please check the URL or scraper.")
            return

        company, position, about, offer_list = offer_information
        offer_text = ' '.join(offer_list) if isinstance(offer_list, list) else ""

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

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_status_color(status):
    """Returns a lighter color based on the offer status."""
    if status == 3:  # Rejected
        return 'red'  # Light red
    elif status == 4:  # Accepted
        return 'green'  # Light green
    elif status == 1:  # Open
        return 'yellow'  # Light yellow
    elif status == 2:  # Applied
        return 'lightblue'  # Light blue
    return 'white'  # Default for "None" or unknown statuses

def open_offers(user_id):
    """Opens the window displaying the user's offers."""
    root = tk.Tk()
    root.title("Your Offers")
    center_window(root, 1024, 768)

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Create a canvas and scrollbar to make the offers list scrollable
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  # Set the scroll region dynamically
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind the mouse wheel to the canvas scroll
    def on_mouse_wheel(event):
        """Handles mouse wheel scrolling for the canvas."""
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # Bind to canvas for scrollwheel events
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows and macOS
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))  # Linux
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))  # Linux

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    offers_frame = tk.Frame(scrollable_frame)
    offers_frame.pack(pady=10, fill="both", expand=True)

    # Adjusted column spans for wider "Position" and "Company"
    tk.Label(offers_frame, text="Position", width=35, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky="ew")
    tk.Label(offers_frame, text="Company", width=35, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=1, columnspan=3, sticky="ew")
    tk.Label(offers_frame, text="Actions", font=("Arial", 10, "bold")).grid(row=0, column=3)

    for idx, offer in enumerate(fetch_offers(user_id)):
        offer_id, position, company, status, response = offer
        status_color = get_status_color(status)

        tk.Label(offers_frame, text=position, width=35, anchor="w", bg=status_color).grid(row=idx + 1, column=0, sticky="ew")
        tk.Label(offers_frame, text=company, width=35, anchor="w", bg=status_color).grid(row=idx + 1, column=1, sticky="ew")
        tk.Button(offers_frame, text="Select", command=lambda offer_id=offer_id: (root.destroy(), open_offer_details(offer_id, user_id))).grid(row=idx + 1, column=2)
        tk.Button(offers_frame, text="Delete", command=lambda offer_id=offer_id: (root.destroy(), delete_offer(offer_id, user_id))).grid(row=idx + 1, column=3)

    # Frame for URL input and scraping button
    scraper_frame = tk.Frame(root)
    scraper_frame.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(scraper_frame, text="Enter URL to scrape offer:", anchor="w").grid(row=0, column=0)
    url_entry = tk.Entry(scraper_frame, width=50)
    url_entry.grid(row=0, column=1)
    tk.Button(scraper_frame, text="Scrape Offer", command=lambda: scrape_offer(user_id, url_entry, root)).grid(row=0, column=2)

    # Back and New Offer buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", padx=20, pady=(10, 0))

    tk.Button(button_frame, text="Back", command=lambda: (root.destroy(), open_menu(user_id))).pack(side="left", padx=(0, 10))
    tk.Button(button_frame, text="New Offer", command=lambda: (root.destroy(), open_new_offer(user_id))).pack(side="left")

    root.mainloop()

# Call the function to open offers for a specific user (example user ID)
# open_offers(user_id=1)  # You can call this function from your main application logic
