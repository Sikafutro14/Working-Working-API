import customtkinter as ctk
from p_data import open_p_data
from offers import open_offers
from main import open_login

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
    open_p_data(user_id)

def open_offers(user_id):
    """Opens the Offers window."""
    root.destroy()
    open_offers(user_id)

def logout():
    """Handles user logout."""
    root.destroy()
    open_login()

def quit_app():
    """Quits the application."""
    root.destroy()

def open_menu(user_id):
    """Opens the Menu window."""
    global root
    root = ctk.CTk()  # Use CTk instead of Tk
    root.title("Menu")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    # Apply CustomTkinter theme
    ctk.set_appearance_mode("dark")  # Options are "dark" or "light"
    ctk.set_default_color_theme("blue")  # You can choose other themes as well

    # Create buttons using CustomTkinter
    personal_data_button = ctk.CTkButton(root, text="Personal Data", command=lambda: open_personal_data(user_id))
    personal_data_button.pack(pady=10)

    offers_button = ctk.CTkButton(root, text="Offers", command=lambda: open_offers(user_id))
    offers_button.pack(pady=10)

    logout_button = ctk.CTkButton(root, text="Logout", command=logout)
    logout_button.pack(pady=10)

    quit_button = ctk.CTkButton(root, text="Quit", command=quit_app)
    quit_button.pack(pady=10)

    root.mainloop()
