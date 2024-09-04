import psycopg2
from tkinter import messagebox
from faker import Faker
import tkinter as tk

class ApplicationTrackerOffers:
    def __init__(self, app):
        self.app = app
        self.db_connection = self.connect_to_database()
        if self.db_connection:
            self.db_cursor = self.db_connection.cursor()

    def connect_to_database(self):
        try:
            # Update with your actual database credentials
            conn = psycopg2.connect(
                dbname="job_app_db",
                user="postgres",
                password="password",
                host="localhost",
                port="5432"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
            return None

    def create_offers_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
        """
        self.execute_query(create_table_query)

    def execute_query(self, query, params=None):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, params)
                self.db_connection.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to execute query: {e}")

    def fetch_offers(self):
        try:
            self.db_cursor.execute("SELECT * FROM offers")
            return self.db_cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch offers: {e}")
            return []

    def create_offer(self):
        title = self.app.offer_entry.get().strip()
        if title:
            self.execute_query("INSERT INTO offers (title) VALUES (%s)", (title,))
            self.display_offers()
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def update_offer(self):
        # For simplicity, assume offer_id is fetched from listbox or another input field.
        offer_id = 1
        title = self.app.offer_entry.get().strip()
        if title:
            self.execute_query("UPDATE offers SET title = %s WHERE id = %s", (title, offer_id))
            self.display_offers()
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def delete_offer(self):
        # For simplicity, assume offer_id is fetched from listbox or another input field.
        offer_id = 1
        self.execute_query("DELETE FROM offers WHERE id = %s", (offer_id,))
        self.display_offers()

    def display_offers(self):
        offers = self.fetch_offers()
        self.app.offers_listbox.delete(0, tk.END)
        if offers:
            for offer in offers:
                offer_str = f"ID: {offer[0]}, Title: {offer[1]}"
                self.app.offers_listbox.insert(tk.END, offer_str)
        else:
            self.app.offers_listbox.insert(tk.END, "No offers available")

    def populate_db_with_fake_data(self):
        fake = Faker()
        for _ in range(10):
            title = fake.company()  # Generate a fake company name as the offer title
            self.execute_query("INSERT INTO offers (title) VALUES (%s)", (title,))
