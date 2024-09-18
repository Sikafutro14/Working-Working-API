import customtkinter as ctk
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to port 5432 if not specified

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def open_offers(user_id):
    """Fetch job offers for a specific user and display them in a CTk window."""
    root = ctk.CTk()
    root.title("Offers")

    window_width = 1024
    window_height = 768
    center_window(root, window_width, window_height)

    # Frame to hold the table
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Create the table (treeview)
    tree = ctk.CTkTreeview(frame, columns=("id", "position", "company", "status"), show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Configure the treeview headings
    tree.heading("id", text="ID")
    tree.heading("position", text="Position")
    tree.heading("company", text="Company")
    tree.heading("status", text="Status")

    # Set column width and alignment
    tree.column("id", width=50, anchor="center")
    tree.column("position", width=200)
    tree.column("company", width=200)
    tree.column("status", width=100, anchor="center")

    # Configure frame for resizing
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Load data from the database
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT id, position, company, status FROM offers WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Insert the data into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

    except psycopg2.Error as e:
        # Display database error using a customtkinter message box
        ctk.CTkMessageBox.show_error("Database Error", f"An error occurred while fetching offers: {e}")

    # Button to open the letter window
    open_letter_button = ctk.CTkButton(root, text="Open Letter", 
                                       command=lambda: open_letter_window(user_id, get_selected_offer(tree)))
    open_letter_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    # Exit button
    exit_button = ctk.CTkButton(root, text="Exit", command=root.destroy)
    exit_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    root.mainloop()

def get_selected_offer(tree):
    """Helper function to get the selected offer ID from the treeview."""
    selected_item = tree.selection()
    if selected_item:
        return tree.item(selected_item)["values"][0]  # Return the offer ID
    return None

def load_letter_from_database(user_id, offer_id):
    """Load the letter content from the database based on the user and offer IDs."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT resume FROM applications WHERE user_id = %s AND offer_id = %s", (user_id, offer_id))
        letter_text = cur.fetchone()
        cur.close()
        conn.close()

        if letter_text:
            return letter_text[0]  # Return the text of the letter
        else:
            ctk.CTkMessageBox.show_warning("No Letter", "No letter found for the selected offer.")
            return ""
    except psycopg2.Error as e:
        ctk.CTkMessageBox.show_error("Database Error", f"An error occurred while retrieving the letter: {e}")
        return ""

def open_letter_window(user_id, offer_id):
    """Open a new window to display the application letter for the selected offer."""
    if offer_id is None:
        ctk.CTkMessageBox.show_warning("Selection Error", "Please select an offer to view the letter.")
        return

    letter_window = ctk.CTk()
    letter_window.title("Application Letter")

    # Create a CTkTextbox to display the letter content
    letter_text_box = ctk.CTkTextbox(letter_window, width=800, height=400, fg_color="gray25", text_color="white")
    letter_text_box.pack(fill="both", expand=True, padx=20, pady=20)

    # Load the letter content from the database
    letter_text = load_letter_from_database(user_id, offer_id)
    letter_text_box.insert("1.0", letter_text)

    # Create a button to close the window
    close_button = ctk.CTkButton(letter_window, text="Close", command=letter_window.destroy)
    close_button.pack(pady=10)

    letter_window.mainloop()

