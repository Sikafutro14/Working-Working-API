import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from ai_module.letter_generator import generate_application_letter

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

def save_offer(offer_id, user_id, position, company, offer_text, about_company, url, response, status):
    """Saves the offer details into the database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("""
            UPDATE offers
            SET position = %s, company = %s, offer = %s, about = %s, url = %s, response = %s, status = %s
            WHERE id = %s AND user_id = %s
        """, (position, company, offer_text, about_company, url, response, status, offer_id, user_id))

        conn.commit()
        messagebox.showinfo("Success", "Offer saved successfully")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving the offer: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def open_offers_window(user_id):
    """Returns to the offers window."""
    import offers  # Assuming offers.py has the function to display the offers list
    offers.open_offers(user_id)

def generate_letter(user_id, position, company, about_company, offer):
    """Calls the generate_application_letter function and stores the letter in the database."""
    try:
        letter = generate_application_letter(user_id, position, company, about_company, offer)

        # Insert or update the letter in the applications table
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        cur.execute("""
            UPDATE applications
            SET resume = %s
            WHERE user_id = %s AND position = %s AND company = %s
        """, (letter, user_id, position, company))

        conn.commit()

        messagebox.showinfo("Success", "Letter generated and saved successfully.")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while generating the letter: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def open_offer(offer_id, user_id):
    """Opens the detailed offer view for a specific offer."""
    offer_window = tk.Toplevel()
    offer_window.title("Offer Details")

    window_width = 1024
    window_height = 768
    center_window(offer_window, window_width, window_height)

    # Fetch offer details from the database
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("SELECT position, company, offer, about, url, response, status FROM offers WHERE id = %s", (offer_id,))
        offer_data = cur.fetchone()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while retrieving the offer: {e}")
        offer_window.destroy()
        return

    # Create input fields
    tk.Label(offer_window, text="Position").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    position_entry = tk.Entry(offer_window, width=80)
    position_entry.grid(row=0, column=1, padx=10, pady=5)
    position_entry.insert(0, offer_data[0])

    tk.Label(offer_window, text="Company").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    company_entry = tk.Entry(offer_window, width=80)
    company_entry.grid(row=1, column=1, padx=10, pady=5)
    company_entry.insert(0, offer_data[1])

    tk.Label(offer_window, text="Offer").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
    offer_text = tk.Text(offer_window, width=80, height=10)
    offer_text.grid(row=2, column=1, padx=10, pady=5)
    offer_text.insert("1.0", offer_data[2])

    tk.Label(offer_window, text="About the Company").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    about_company_text = tk.Text(offer_window, width=80, height=10)
    about_company_text.grid(row=3, column=1, padx=10, pady=5)
    about_company_text.insert("1.0", offer_data[3])

    tk.Label(offer_window, text="URL").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    url_entry = tk.Entry(offer_window, width=80)
    url_entry.grid(row=4, column=1, padx=10, pady=5)
    url_entry.insert(0, offer_data[4])

    # Response (True/False) using radio buttons
    tk.Label(offer_window, text="Response").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    response_var = tk.BooleanVar(value=offer_data[5])
    tk.Radiobutton(offer_window, text="True", variable=response_var, value=True).grid(row=5, column=1, padx=5, sticky="w")
    tk.Radiobutton(offer_window, text="False", variable=response_var, value=False).grid(row=5, column=1, padx=60, sticky="w")

    # Status using dropdown
    tk.Label(offer_window, text="Status").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    status_var = tk.StringVar(offer_window)
    status_options = {1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}
    status_menu = ttk.Combobox(offer_window, textvariable=status_var, values=list(status_options.values()))
    status_menu.grid(row=6, column=1, padx=10, pady=5)
    status_menu.set(status_options[offer_data[6]])

    # Buttons
    button_frame = tk.Frame(offer_window)
    button_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")

    def save():
        """Handles the save button click event."""
        position = position_entry.get()
        company = company_entry.get()
        offer = offer_text.get("1.0", tk.END).strip()
        about_company = about_company_text.get("1.0", tk.END).strip()
        url = url_entry.get()
        response = response_var.get()
        status = list(status_options.keys())[list(status_options.values()).index(status_menu.get())]
        save_offer(offer_id, user_id, position, company, offer, about_company, url, response, status)

    save_button = tk.Button(button_frame, text="Save", command=save)
    save_button.pack(side="left", padx=10)

    back_button = tk.Button(button_frame, text="Back", command=lambda: (offer_window.destroy(), open_offers_window(user_id)))
    back_button.pack(side="left", padx=10)

    generate_button = tk.Button(button_frame, text="Generate Letter", command=lambda: generate_letter(user_id, position_entry.get(), company_entry.get(), about_company_text.get("1.0", tk.END).strip(), offer_text.get("1.0", tk.END).strip()))
    generate_button.pack(side="left", padx=10)

    offer_window.mainloop()
