import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def create_offers_table():
    """Create the offers table in the database if it does not exist."""
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        
        # SQL command to create the offers table
        create_table_command = """
        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            position VARCHAR(255) NOT NULL,
            company VARCHAR(255) NOT NULL,
            offer TEXT NOT NULL,
            about TEXT,
            url VARCHAR(255),
            status BOOLEAN NOT NULL DEFAULT FALSE,
            response BOOLEAN NOT NULL DEFAULT FALSE,
            user_id INTEGER REFERENCES users(id)
        )
        """
        
        # Execute the command to create the table
        cur.execute(create_table_command)
        conn.commit()
        print("Offers table created successfully.")
        
    except Exception as e:
        # Log the error securely
        print("Error creating offers table.")
        print(f"Details: {str(e)}")
    
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

def open_offers(username=None):
    """Fetch job offers for a specific user and return them as a formatted string."""
    
    offers_str = ""

    try:
        # Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Fetch offers from the database for the given user
        cur.execute("""
            SELECT * 
            FROM offers 

        """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        if rows:
            # Format each offer into a string and append it to offers_str
            for row in rows:
                position, company, offer, about, url, status, response = row
                offers_str += (
                    f"Position: {position}\n"
                    f"Company: {company}\n"
                    f"Offer: {offer}\n"
                    f"About: {about}\n"
                    f"URL: {url}\n"
                    f"Status: {'Accepted' if status else 'Pending'}\n"
                    f"Response: {'Yes' if response else 'No'}\n"
                    "------------------------------------------\n"
                )
        else:
            offers_str = "No offers available for this user."

    except psycopg2.Error as e:
        offers_str = f"Error fetching offers: {str(e)}"

    return offers_str

# Ensure the offers table exists when this script is executed
if __name__ == "__main__":
    create_offers_table()




