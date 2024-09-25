import tkinter as tk
from tkinter import messagebox, END
import psycopg2
import customtkinter as ctk

# CustomTkinter settings
ctk.set_appearance_mode("dark")  # Initial mode is dark
ctk.set_default_color_theme("Nessa/CTK_THEMES/blue.json")  # Use custom theme

# Database configuration
DB_NAME = "k47a"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"

# Function to center the window
def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to toggle between dark and light mode
mode = "dark"  # Track current mode

def toggle_mode():
    global mode
    if mode == "dark":
        ctk.set_appearance_mode("light")
        mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        mode = "dark"

# Function to fetch user statistics
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
                COUNT(CASE WHEN a.id IS NOT NULL THEN 1 END) AS total_applications
            FROM users u
            LEFT JOIN offers o ON u.id = o.user_id
            LEFT JOIN applications a ON o.id = a.offer_id
            WHERE u.id = %s
            GROUP BY u.id;
        """, (user_id,))

        user_stats = cur.fetchone()

        if user_stats:
            total_offers, responded_offers, total_applications = user_stats
            stats_text.set(f"Total Offers: {total_offers}\nResponded Offers: {responded_offers}\nTotal Applications: {total_applications}")
        else:
            stats_text.set("No data available")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open personal data (just a placeholder)
def open_personal_data(user_id):
    messagebox.showinfo("Personal Data", "Opening Personal Data...")

# Function to open offers (just a placeholder)
def open_offers(user_id):
    messagebox.showinfo("Offers", "Opening Offers...")

# Function to open AI Assistant (just a placeholder)
def chat_gpt(user_id):
    messagebox.showinfo("AI Assistant", "Opening AI Assistant...")

# Function to open search (just a placeholder)
def open_search(user_id):
    messagebox.showinfo("Search", "Opening Search...")

# Function to logout (just a placeholder)
def logout():
    messagebox.showinfo("Logout", "Logging out...")
    root.destroy()

# Function to quit the application
def quit_app():
    root.destroy()

# Main function to open the menu
def open_menu(user_id):
    global root, stats_text

    root = ctk.CTk()  # Use CustomTkinter root
    root.title("User Dashboard")

    window_width = 1024
    window_height = 768
    center_window(root, window_width, window_height)

    # Top frame for the search bar and theme toggle
    top_frame = ctk.CTkFrame(root, height=100)
    top_frame.pack(fill="x", padx=20, pady=10)

    search_entry = ctk.CTkEntry(top_frame, width=500, placeholder_text="Search")
    search_entry.pack(side=tk.LEFT, padx=10, pady=10)

    search_button = ctk.CTkButton(top_frame, text="Search", command=lambda: open_search(user_id))
    search_button.pack(side=tk.LEFT, padx=10, pady=10)

    mode_toggle_button = ctk.CTkButton(top_frame, text="Toggle Light/Dark", command=toggle_mode)
    mode_toggle_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Left frame for navigation buttons
    left_frame = ctk.CTkFrame(root, width=200)
    left_frame.pack(side=tk.LEFT, fill="y", padx=20, pady=20)

    personal_data_button = ctk.CTkButton(left_frame, text="Personal Data", command=lambda: open_personal_data(user_id))
    personal_data_button.pack(pady=10)

    offers_button = ctk.CTkButton(left_frame, text="Offers", command=lambda: open_offers(user_id))
    offers_button.pack(pady=10)

    ai_assistant_button = ctk.CTkButton(left_frame, text="AI Assistant", command=lambda: chat_gpt(user_id))
    ai_assistant_button.pack(pady=10)

    search_button = ctk.CTkButton(left_frame, text="Search", command=lambda: open_search(user_id))
    search_button.pack(pady=10)

    logout_button = ctk.CTkButton(left_frame, text="Logout", command=logout)
    logout_button.pack(pady=10)

    quit_button = ctk.CTkButton(left_frame, text="Quit", command=quit_app)
    quit_button.pack(pady=10)

    # Dashboard on the right side
    dashboard_frame = ctk.CTkFrame(root)
    dashboard_frame.pack(side=tk.LEFT, padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(dashboard_frame, text="Dashboard", font=("Arial", 18)).pack(pady=10)

    stats_text = tk.StringVar()
    ctk.CTkLabel(dashboard_frame, textvariable=stats_text, font=("Arial", 14), justify=tk.LEFT).pack(pady=10)

    # Load user stats into the dashboard
    load_user_dashboard(user_id)

    root.mainloop()

# Start the application with a user ID
open_menu(user_id=1)  # Replace with the appropriate user ID for testing
