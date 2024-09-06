import psycopg2
from tkinter import messagebox
from faker import Faker
import tkinter as tk
import random
import customtkinter as ctk

class ApplicationTrackerOffers:
    def __init__(self, app, scrollable_frame= None):
        self.app = app
        self.scrollable_frame = scrollable_frame
        self.db_connection = self.connect_to_database()
        if self.db_connection:
            self.db_cursor = self.db_connection.cursor()

    def connect_to_database(self):
        try:
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
            user_id INTEGER,
            company TEXT,
            department TEXT,
            offer_url TEXT,
            company_description TEXT,
            offer_text TEXT,
            status INTEGER,
            response TEXT,
            title TEXT
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

    def display_offers(self):
        offers = self.fetch_offers()

        # Clear existing data
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add headers
        headers = ["ID", "Company", "Department", "Offer URL", "Company Description", "Offer Text", "Status", "Response", "Title"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Roboto", 12, "bold"),
                                width=120, height=30, fg_color=self.app.accent_color, text_color=self.app.white)
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        # Add rows
        if offers:
            for i, offer in enumerate(offers):
                for j, data in enumerate(offer):
                    # Access data using correct column index
                    data_to_display = str(data)  # Handle data type conversion if needed
                    label = ctk.CTkLabel(self.scrollable_frame, text=data_to_display, font=("Roboto", 12),
                                        width=120, height=30, fg_color=self.app.white, text_color=self.app.dark_blue)
                    label.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)
                    self.scrollable_frame.grid_columnconfigure(j, weight=1)
        else:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="No offers available", font=("Roboto", 12), text_color=self.app.dark_blue)
            empty_label.grid(row=1, column=0, columnspan=len(headers), pady=20)
    def create_offer(self):
        title = self.app.offer_entry.get().strip()
        if title:
            self.execute_query("INSERT INTO offers (offer_text) VALUES (%s)", (title,))
            self.display_offers()  # Update the GUI
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def update_offer(self):
        offer_id = 1
        title = self.app.offer_entry.get().strip()
        if title:
            self.execute_query("UPDATE offers SET offer_text = %s WHERE id = %s", (title, offer_id))
            self.display_offers()  # Update the GUI
        else:
            messagebox.showerror("Input Error", "Offer title cannot be empty.")

    def delete_offer(self):
        offer_id = 1
        self.execute_query("DELETE FROM offers WHERE id = %s", (offer_id,))
        self.display_offers()  # Update the GUI

    def populate_db_with_fake_data(self):
        fake = Faker()
        for _ in range(100):
            company = fake.company()
            department = fake.bs()
            offer_url = fake.url()
            company_description = fake.text(max_nb_chars=200)
            offer_text = fake.text(max_nb_chars=500)
            status = fake.random_int(min=0, max=2)
            response = bool(random.getrandbits(1))
            title = fake.job()

            self.execute_query("""
                INSERT INTO offers (company, department, offer_url, company_description, offer_text, status, response, title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (company, department, offer_url, company_description, offer_text, status, response, title))
            
        self.db_connection.commit()


    
