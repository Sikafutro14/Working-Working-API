import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

DB_NAME = "ak47"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"

# Status options for mapping integers to text
status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}

# Global variables
user_id = None
position_var = None
company_var = None
status_var = None

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def create_view():
    """Creates the view for offers if it does not exist."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE OR REPLACE VIEW offer_details_view AS
            SELECT 
                o.id,
                o.position,
                o.company,
                o.offer,
                o.status,
                u.username AS user_name
            FROM 
                offers o
            JOIN 
                users u ON o.user_id = u.id;
        """)
        print(cur.execute('''select * from offer_details_view;'''))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating view: {e}")

def fetch_filter_options():
    """Fetches distinct filter options (positions, companies) from the database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Fetch distinct positions
        cur.execute("SELECT DISTINCT position FROM offers")
        positions = [row[0] for row in cur.fetchall()]

        # Fetch distinct companies
        cur.execute("SELECT DISTINCT company FROM offers")
        companies = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return positions, companies
    except Exception as e:
        print(f"Error fetching filter options: {e}")
        return [], []

def search_offers(filters):
    """Performs a search on the offers based on the provided filters."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Query the view 'offer_details_view'
        query = "SELECT id, position, company, offer, status FROM offer_details_view WHERE 1=1"
        params = []

        # Apply filters only if they're not "Any"
        if filters.get("position") != "Any":
            query += " AND position = %s"
            params.append(filters['position'])
        
        if filters.get("company") != "Any":
            query += " AND company = %s"
            params.append(filters['company'])

        if filters.get("status") != "Any":
            # Get the corresponding integer for the selected status
            for key, value in status_options.items():
                if value == filters['status']:
                    query += " AND status = %s"
                    params.append(key)
                    break

        cur.execute(query, params)
        results = cur.fetchall()

        cur.close()
        conn.close()

        return results
    except Exception as e:
        print(f"Error searching offers: {e}")
        return []

def perform_search():
    """Handles the search button click."""
    filters = {
        "position": position_var.get(),
        "company": company_var.get(),
        "status": status_var.get()
    }
    
    results = search_offers(filters)
    if results:
        # Import and open the search results window
        from search_results import open_search_results
        open_search_results(results, user_id)  # Pass user_id to the results function
    else:
        messagebox.showinfo("No Results", "No matching offers found.")

def open_search(uid):
    """Opens the Search window."""
    global user_id, position_var, company_var, status_var

    user_id = uid  # Assign the passed user_id to the global variable
    create_view()  # Create the view if it doesn't exist

    root = tk.Tk()
    root.title("Search Offers")
    window_width = 1024
    window_height = 768
    center_window(root, window_width, window_height)

    # Fetch filter options
    positions, companies = fetch_filter_options()

    # Create dropdowns for search options
    tk.Label(root, text="Position").grid(row=0, column=0, padx=10, pady=10)
    position_var = tk.StringVar(value="Any")
    position_dropdown = ttk.Combobox(root, textvariable=position_var, values=["Any"] + positions, state="readonly")
    position_dropdown.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Company").grid(row=1, column=0, padx=10, pady=10)
    company_var = tk.StringVar(value="Any")
    company_dropdown = ttk.Combobox(root, textvariable=company_var, values=["Any"] + companies, state="readonly")
    company_dropdown.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Status").grid(row=2, column=0, padx=10, pady=10)
    status_var = tk.StringVar(value="Any")
    status_dropdown = ttk.Combobox(root, textvariable=status_var, values=["Any"] + list(status_options.values()), state="readonly")
    status_dropdown.grid(row=2, column=1, padx=10, pady=10)

    # Search and Back Buttons
    tk.Button(root, text="Search", command=perform_search).grid(row=3, column=1, padx=10, pady=10)
    
    # Back button reloads the menu and destroys the search window
    tk.Button(root, text="Back", command=lambda: (root.destroy(), reload_menu(user_id))).grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()

def reload_menu(user_id):
    """Reload the menu when back is pressed."""
    from menu import open_menu
    open_menu(user_id)
