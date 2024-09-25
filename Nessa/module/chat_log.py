import os
import psycopg2
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv

# Function to center the window on the screen
def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def open_log(user_id):
    # Load environment variables (DB credentials)
    load_dotenv()

    # PostgreSQL connection setup
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()

    # Fetch chat log entries for the specific user
    cursor.execute("SELECT user_input, assistant_response, created_at FROM chat_log WHERE user_id = %s", (user_id,))
    logs = cursor.fetchall()

    # Close the connection
    conn.close()

    # Tkinter window setup
    log_window = tk.Tk()
    log_window.title(f"Chat Log for User ID {user_id}")

    window_width = 1024
    window_height = 768
    center_window(log_window, window_width, window_height)

    # ScrolledText to display logs
    log_display = ScrolledText(log_window, wrap=tk.WORD, state=tk.NORMAL, bg="white", fg="black", font=("Arial", 12))
    log_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Insert the fetched logs into the ScrolledText widget
    for log in logs:
        log_display.insert(tk.END, f"Timestamp: {log[2]}\n")
        log_display.insert(tk.END, f"User: {log[0]}\n")
        log_display.insert(tk.END, f"Assistant: {log[1]}\n\n")

    # Disable editing of the text box after inserting logs
    log_display.config(state=tk.DISABLED)

    # Back button to close log window
    def on_back():
        log_window.destroy()

    back_button = tk.Button(log_window, text="Back", command=on_back, font=("Arial", 12))
    back_button.pack(pady=5)

    log_window.mainloop()
