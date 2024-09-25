import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from ai_module.letter_generator import generate_application_letter
import letter 

# Database connection parameters
DB_NAME = "k47a"
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

def generate_letter(user_id, offer_id):
    """Calls the generate_application_letter function and stores the letter in the database."""
    
    try:
        # Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Fetch user's first name, last name, and background info from p_info table
        cur.execute("SELECT first_name, last_name, background FROM p_info WHERE user_id = %s", (user_id,))
        p_info_data = cur.fetchone()
        if not p_info_data:
            messagebox.showerror("Error", "Personal information not found for the user.")
            return
        
        first_name, last_name, background = p_info_data
        name = f"{first_name} {last_name}"  # Concatenate first and last name

        # Fetch offer details from offers table
        cur.execute("SELECT position, company, about, offer FROM offers WHERE id = %s", (offer_id,))
        offer_data = cur.fetchone()
        if not offer_data:
            messagebox.showerror("Error", "Offer information not found.")
            return
        
        position, company, about_company, offer_text = offer_data

        # Generate the letter
        letter = generate_application_letter(
            name,
            background,
            position,
            company,
            about_company,
            offer_text
        )

        # Check if the record already exists in the applications table
        cur.execute("SELECT id FROM applications WHERE user_id = %s AND offer_id = %s", (user_id, offer_id))
        existing_record = cur.fetchone()

        if existing_record:
            # Update existing record
            cur.execute("""
                UPDATE applications
                SET resume = %s
                WHERE user_id = %s AND offer_id = %s
            """, (letter, user_id, offer_id))
        else:
            # Insert new record
            cur.execute("""
                INSERT INTO applications (user_id, offer_id, resume)
                VALUES (%s, %s, %s)
            """, (user_id, offer_id, letter))

        conn.commit()
        messagebox.showinfo("Success", "Letter generated and saved successfully.")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while generating the letter: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def view_letter(user_id, offer_id):
    """Opens the letter view window."""
    letter.open_letter_window(user_id, offer_id)

def open_offer(offer_id, user_id):
    """Opens the detailed offer view for a specific offer."""
    root = tk.Tk()
    root.title("Offer Details")

    window_width = 1024
    window_height = 768
    center_window(root, window_width, window_height)

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
        root.destroy()
        return

    # Create input fields
    tk.Label(root, text="Position").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    position_entry = tk.Entry(root, width=80)
    position_entry.grid(row=0, column=1, padx=10, pady=5)
    position_entry.insert(0, offer_data[0])

    tk.Label(root, text="Company").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    company_entry = tk.Entry(root, width=80)
    company_entry.grid(row=1, column=1, padx=10, pady=5)
    company_entry.insert(0, offer_data[1])

    tk.Label(root, text="Offer").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
    offer_text = tk.Text(root, width=80, height=10)
    offer_text.grid(row=2, column=1, padx=10, pady=5)
    offer_text.insert("1.0", offer_data[2])

    tk.Label(root, text="About the Company").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    about_company_text = tk.Text(root, width=80, height=10)
    about_company_text.grid(row=3, column=1, padx=10, pady=5)
    about_company_text.insert("1.0", offer_data[3])

    tk.Label(root, text="URL").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    url_entry = tk.Entry(root, width=80)
    url_entry.grid(row=4, column=1, padx=10, pady=5)
    url_entry.insert(0, offer_data[4])

    # Response (True/False) using radio buttons
    tk.Label(root, text="Response").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    response_var = tk.BooleanVar(value=offer_data[5])
    tk.Radiobutton(root, text="True", variable=response_var, value=True).grid(row=5, column=1, padx=5, sticky="w")
    tk.Radiobutton(root, text="False", variable=response_var, value=False).grid(row=5, column=1, padx=60, sticky="w")

    # Status using dropdown
    tk.Label(root, text="Status").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    status_var = tk.StringVar(root)
    status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}
    status_menu = ttk.Combobox(root, textvariable=status_var, values=list(status_options.values()))
    status_menu.grid(row=6, column=1, padx=10, pady=5)
    status_menu.set(status_options.get(offer_data[6], "None"))

    # Buttons
    button_frame = tk.Frame(root)
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

    back_button = tk.Button(button_frame, text="Back", command=lambda: (root.destroy(), open_offers_window(user_id)))
    back_button.pack(side="left", padx=10)

    generate_button = tk.Button(button_frame, text="Generate Letter", command=lambda: generate_letter(user_id, offer_id))
    generate_button.pack(side="left", padx=10)

    view_letter_button = tk.Button(button_frame, text="View Letter", command=lambda: view_letter(user_id, offer_id))
    view_letter_button.pack(side="left", padx=10)

    root.mainloop()
