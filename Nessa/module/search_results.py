import tkinter as tk

status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def open_search_results(results):
    """Displays the search results in a new window."""
    result_window = tk.Tk()
    result_window.title("Search Results")
    window_width = 1024
    window_height = 768
    center_window(result_window, window_width, window_height)

    # Create a frame to hold the results
    result_frame = tk.Frame(result_window)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Display each result in a new label
    for idx, result in enumerate(results):
        position, company, offer, status = result
        status_text = status_options.get(status, "Unknown")
        result_text = f"{idx+1}. Position: {position}, Company: {company}, Status: {status_text}"
        tk.Label(result_frame, text=result_text, anchor="w").pack(padx=10, pady=5, fill=tk.X)

    # Add a Close button to close the results window
    tk.Button(result_frame, text="Close", command=result_window.destroy).pack(pady=10)

    result_window.mainloop()
