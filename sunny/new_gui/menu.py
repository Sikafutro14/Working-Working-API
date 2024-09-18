import tkinter as tk

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

def logout():
    """Handles user logout."""
    root.destroy()
    from main import open_login
    root.destroy()
    open_login()

def quit_app():
    """Quits the application."""
    root.destroy()

def open_menu(user_id):
    """Opens the Menu window."""
    global root
    root = tk.Tk()
    root.title("Menu")

    window_width = 1024
    window_height = 768
    
    center_window(root, window_width, window_height)

    tk.Button(root, text="Personal Data", command=lambda: open_personal_data(user_id)).pack(pady=10)
    tk.Button(root, text="Offers", command=lambda: open_offers(user_id)).pack(pady=10)
    tk.Button(root, text="Logout", command=logout).pack(pady=10)
    tk.Button(root, text="Quit", command=quit_app).pack(pady=10)

    root.mainloop()
