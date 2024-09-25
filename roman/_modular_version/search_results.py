import tkinter as tk
from tkinter import messagebox

status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def open_offer_details(offer_id, user_id):
    import offer  # Make sure the offer module is correctly imported
    offer.open_offer(offer_id, user_id)  # Pass both offer_id and user_id to open_offer

def open_search_results(results, user_id):
    """Displays the search results in a new window."""
    result_window = tk.Tk()
    result_window.title("Search Results")
    window_width = 1024
    window_height = 768
    center_window(result_window, window_width, window_height)

    # Create a frame to hold the results
    result_frame = tk.Frame(result_window)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Display each result in a new label and button
    for idx, result in enumerate(results):
        offer_id, position, company, offer, status = result
        status_text = status_options.get(status, "Unknown")
        
        # Create a frame for each offer result
        offer_frame = tk.Frame(result_frame)
        offer_frame.pack(fill=tk.X, padx=10, pady=5)

        result_text = f"{idx+1}. Position: {position}, Company: {company}, Status: {status_text}"
        tk.Label(offer_frame, text=result_text, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Select button
        select_button = tk.Button(offer_frame, text="Select", command=lambda id=offer_id: open_offer_details(id, user_id))
        select_button.pack(side=tk.RIGHT)

    # Add a Close button to close the results window
    tk.Button(result_frame, text="Close", command=result_window.destroy).pack(pady=10)

    result_window.mainloop()
