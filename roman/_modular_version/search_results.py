import tkinter as tk
from tkinter import ttk, messagebox

status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}

def open_offer_details(offer_id, user_id):
    import offer  # Make sure the offer module is correctly imported
    offer.open_offer(offer_id, user_id)  # Pass both offer_id and user_id to open_offer

def open_search_results(results, user_id):
    """Displays the search results in a new window with a table for view data."""
    result_window = tk.Tk()
    result_window.title("Search Results")
    window_width = 1024
    window_height = 768
    center_window(result_window, window_width, window_height)

    # Create frames for results and table
    result_frame = tk.Frame(result_window)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    table_frame = tk.Frame(result_frame)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Display each search result as text
    for idx, result in enumerate(results):
        offer_id, position, company, offer, status = result
        status_text = status_options.get(status, "Unknown")

        result_text = f"{idx+1}. Position: {position}, Company: {company}, Status: {status_text}"
        tk.Label(result_frame, text=result_text, anchor="w").pack(side=tk.TOP, fill=tk.X, expand=True)

        # Select button
        select_button = tk.Button(result_frame, text="Select", command=lambda id=offer_id: open_offer_details(id, user_id))
        select_button.pack(side=tk.TOP)

    # Create a table to display the view data
    table = ttk.Treeview(table_frame, columns=("id", "position", "company", "offer", "user_name", "status"))
    table.heading("#0", text="ID")
    table.heading("id", text="ID")
    table.heading("position", text="Position")
    table.heading("company", text="Company")
    table.heading("offer", text="Offer")
    table.heading("user_name", text="User Name")
    table.heading("status", text="Status")
    table.column("#0", width=50, minwidth=50, stretch=False)  # Hide the first column
    table.column("id", width=50, minwidth=50, stretch=False)
    table.column("position", width=200, minwidth=200, stretch=True)
    table.column("company", width=200, minwidth=200, stretch=True)
    table.column("offer", width=400, minwidth=400, stretch=True)
    table.column("user_name", width=200, minwidth=200, stretch=True)
    table.column("status", width=100, minwidth=100, stretch=True)
    table.pack(fill=tk.BOTH, expand=True)

    # Fill the table with data from the view (assuming you have a function to fetch view data)
    # This is where you'd use the fetched data from the view
    view_data = fetch_view_data(user_id)  # Replace with your function to fetch view data
    for row in view_data:
        table.insert("", tk.END, values=row)

    # Add a Close button
    tk.Button(result_frame, text="Close", command=result_window.destroy).pack(pady=10)

    result_window.mainloop()