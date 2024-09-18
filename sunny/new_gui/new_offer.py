import customtkinter as ctk
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables for database credentials
load_dotenv()

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


def create_new_offer():
    # Add your logic to create a new offer here
    print("New offer creation logic goes here.")
    return "New offer created successfully."


def save_offer(user_id, position, company, offer_text, about_company, url):
    """Saves the offer details into the database."""
    if not position or not company or not offer_text or not about_company or not url:
        ctk.CTkMessageBox.show_error("Error", "Please fill in all required fields")
        return

    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'), 
            user=os.getenv('DB_USER'), 
            password=os.getenv('DB_PASSWORD'), 
            host=os.getenv('DB_HOST')
        )
        cur = conn.cursor()

        # Insert the offer into the offers table
        cur.execute(
            "INSERT INTO offers (user_id, position, company, offer, about, url) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, position, company, offer_text, about_company, url)
        )
        conn.commit()

        ctk.CTkMessageBox.showinfo("Success", "Offer saved successfully")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        ctk.CTkMessageBox.show_error("Database Error", f"An error occurred while saving the offer: {e}")
    except Exception as e:
        ctk.CTkMessageBox.show_error("Error", f"An unexpected error occurred: {e}")


def open_offers_window(user_id):
    """Returns to the offers window."""
    root.destroy()
    from offers import open_offers
    open_offers(user_id)


def open_new_offer(user_id):
    """Opens the window to create a new offer."""
    global root, position_entry, company_entry, offer_text, about_company_text, url_entry

    root = ctk.CTk()
    root.title("New Offer")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    # Input labels and entries for offer details
    position_label = ctk.CTkLabel(root, text="Position")
    position_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    position_entry = ctk.CTkEntry(root)
    position_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    company_label = ctk.CTkLabel(root, text="Company Name")
    company_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    company_entry = ctk.CTkEntry(root)
    company_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    offer_label = ctk.CTkLabel(root, text="Offer Text")
    offer_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    offer_text = ctk.CTkTextbox(root, wrap="word", width=600, height=300)
    offer_text.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    about_company_label = ctk.CTkLabel(root, text="About the Company")
    about_company_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    about_company_text = ctk.CTkTextbox(root, wrap="word", width=600, height=100)
    about_company_text.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    url_label = ctk.CTkLabel(root, text="URL")
    url_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    url_entry = ctk.CTkEntry(root)
    url_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Save button
    save_button = ctk.CTkButton(root, text="Save", command=lambda: save_offer(
        user_id, position_entry.get(), company_entry.get(), offer_text.get("1.0", "end").strip(), about_company_text.get("1.0", "end").strip(), url_entry.get()))
    save_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Back button
    back_button = ctk.CTkButton(root, text="Back", command=lambda: open_offers_window(user_id))
    back_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    root.mainloop()
