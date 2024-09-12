import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ApplicationTrackerOffers:
    def __init__(self, app):
        self.app = app
        self.connection = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                port=os.getenv('DB_PORT')
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error connecting to the database: {error}")

    def create_offers_table(self):
        """Create the offers table if it doesn't already exist."""
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL
            )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Offers table created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error creating table: {error}")
            self.connection.rollback()

    def create_offer(self, offer_id, company, title):
        """Insert a new offer into the offers table."""
        try:
            insert_query = '''
            INSERT INTO offers (title) VALUES (%s)
            RETURNING id
            '''
            self.cursor.execute(insert_query, (title,))
            self.connection.commit()
            offer_id = self.cursor.fetchone()[0]
            print(f"Offer '{title}' created with ID {offer_id}.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error inserting offer: {error}")
            self.connection.rollback()

    def update_offer(self, offer_id, new_title):
        """Update the title of an offer by its ID."""
        try:
            update_query = '''
            UPDATE offers
            SET title = %s
            WHERE id = %s
            '''
            self.cursor.execute(update_query, (new_title, offer_id))
            self.connection.commit()
            print(f"Offer ID {offer_id} updated to '{new_title}'.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error updating offer: {error}")
            self.connection.rollback()

    def delete_offer(self, offer_id):
        """Delete an offer by its ID."""
        try:
            delete_query = '''
            DELETE FROM offers
            WHERE id = %s
            '''
            self.cursor.execute(delete_query, (offer_id,))
            self.connection.commit()
            print(f"Offer ID {offer_id} deleted.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error deleting offer: {error}")
            self.connection.rollback()

    def fetch_offers(self):
        """Retrieve all offers from the offers table."""
        try:
            select_query = '''
            SELECT id, title FROM offers
            ORDER BY id ASC
            '''
            self.cursor.execute(select_query)
            offers = self.cursor.fetchall()
            return offers
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error fetching offers: {error}")
            return []

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")



    
