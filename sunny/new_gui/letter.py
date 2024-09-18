import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()  # Load database credentials from .env

class LetterWindow(ctk.CTkFrame):
    def __init__(self, master, user_id, offer_id):
        super().__init__(master, fg_color="gray10")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_box = ctk.CTkTextbox(self, wrap="word", width=100, height=30, fg_color="gray25", text_color="white")
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self, fg_color="gray15")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.save_button = ctk.CTkButton(self.button_frame, text="Save", command=self.save_letter)
        self.save_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=lambda: self.master.destroy())
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.user_id = user_id
        self.offer_id = offer_id

        self.load_letter()

    def load_letter(self):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'), 
                user=os.getenv('DB_USER'), 
                password=os.getenv('DB_PASSWORD'), 
                host=os.getenv('DB_HOST')
            )
            cur = conn.cursor()
            cur.execute("SELECT resume FROM applications WHERE user_id = %s AND offer_id = %s", (self.user_id, self.offer_id))
            letter_data = cur.fetchone()

            if not letter_data:
                messagebox.showerror("Error", "No letter found for this offer.")
                self.master.destroy()
                return

            letter_text = letter_data[0]
            self.text_box.insert("1.0", letter_text)

            cur.close()
            conn.close()

        except psycopg2.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while retrieving the letter: {e}")
            self.master.destroy()
            return

    def save_letter(self):
        letter_text = self.text_box.get("1.0", tk.END).strip()
        if letter_text:
            save_letter(self.user_id, self.offer_id, letter_text)
        else:
            messagebox.showerror("Error", "Cannot save an empty letter.")

# Function to save letter in the database
def save_letter(user_id, offer_id, letter_text):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'), 
            user=os.getenv('DB_USER'), 
            password=os.getenv('DB_PASSWORD'), 
            host=os.getenv('DB_HOST')
        )
        cur = conn.cursor()
        cur.execute("""
            UPDATE applications
            SET resume = %s
            WHERE user_id = %s AND offer_id = %s
        """, (letter_text, user_id, offer_id))
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Success", "Letter saved successfully!")

    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving the letter: {e}")
