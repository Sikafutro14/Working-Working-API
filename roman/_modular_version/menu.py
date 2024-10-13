import tkinter as tk
from tkinter import messagebox
import psycopg2

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

def open_personal_data(user_id):
    """Opens the Personal Data window."""
    root.destroy()
    from p_data import open_p_data
    open_p_data(user_id)

def open_offers(user_id):
    """Opens the Offers window."""
    root.destroy()
    from offers import open_offers
    open_offers(user_id)

def chat_gpt(user_id):
    """Opens the Chat."""
    root.destroy()
    from ai_module.chatgpt import help_chatgpt
    help_chatgpt(user_id)

def open_search(user_id):
    """Opens the Search window."""
    root.destroy()
    from search import open_search
    open_search(user_id)

def logout():
    """Handles user logout."""
    root.destroy()
    from main import open_login
    open_login()

def quit_app():
    """Quits the application."""
    root.destroy()

def load_user_dashboard(user_id):
    """Fetches user statistics and displays them in the dashboard."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Fetch user offer statistics
        cur.execute("""
            SELECT 
                COUNT(o.id) AS total_offers,
                COUNT(CASE WHEN o.response = TRUE THEN 1 END) AS responded_offers,
                COUNT(CASE WHEN o.status IS NOT NULL AND o.status != 0 THEN 1 END) AS total_applications,  -- Count all statuses other than 'None'
                COUNT(CASE WHEN o.status = 1 THEN 1 END) AS open_applications,  -- Count for open applications
                COUNT(CASE WHEN o.status = 2 THEN 1 END) AS applied_applications,  -- Count for applied applications
                COUNT(CASE WHEN o.status = 3 THEN 1 END) AS rejected_applications,  -- Count for rejected applications
                COUNT(CASE WHEN o.status = 4 THEN 1 END) AS accepted_applications   -- Count for accepted applications
            FROM users u
            LEFT JOIN offers o ON u.id = o.user_id
            WHERE u.id = %s
            GROUP BY u.id;
        """, (user_id,))

        user_stats = cur.fetchone()

        if user_stats:
            (total_offers, responded_offers, total_applications,
             open_applications, applied_applications, rejected_applications, accepted_applications) = user_stats
             
            # Update stats_text to include all the new information
            stats_text.set(
                f"Total Offers: {total_offers}\n"
                f"Total Applications: {total_applications}\n"
                f"Responded: {responded_offers}\n"
                f"Open Applications: {open_applications}\n"
                f"Rejected Applications: {rejected_applications}\n"
                f"Accepted Applications: {accepted_applications}"
            )
        else:
            stats_text.set("No data available")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_menu(user_id):
    """Opens the Menu window with dashboard and search button."""
    global root, stats_text
    root = tk.Tk()
    root.title("Menu")

    window_width = 1024
    window_height = 768
    
    center_window(root, window_width, window_height)

    # Left side with buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Button(button_frame, text="Personal Data", command=lambda: open_personal_data(user_id)).pack(pady=10)
    tk.Button(button_frame, text="Offers", command=lambda: open_offers(user_id)).pack(pady=10)
    tk.Button(button_frame, text="AI Assistant", command=lambda: chat_gpt(user_id)).pack(pady=10)
    tk.Button(button_frame, text="Search", command=lambda: open_search(user_id)).pack(pady=10)
    tk.Button(button_frame, text="Logout", command=logout).pack(pady=10)
    tk.Button(button_frame, text="Quit", command=quit_app).pack(pady=10)

    # Right side with Dashboard
    dashboard_frame = tk.Frame(root)
    dashboard_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Label(dashboard_frame, text="Dashboard", font=("Arial", 18)).pack(pady=10)

    stats_text = tk.StringVar()
    tk.Label(dashboard_frame, textvariable=stats_text, font=("Arial", 14), justify=tk.LEFT).pack(pady=10)

    # Load user stats into the dashboard
    load_user_dashboard(user_id)

    root.mainloop()
