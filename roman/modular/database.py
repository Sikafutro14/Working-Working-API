import psycopg2
from psycopg2 import sql

def connect_to_db():
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
        print(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personal_info (
            user_id INTEGER PRIMARY KEY REFERENCES users(id),
            email VARCHAR(100),
            cv_path VARCHAR(255),
            skills TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            title VARCHAR(100),
            company VARCHAR(100),
            department VARCHAR(100),
            offer_url TEXT,
            company_description TEXT,
            offer_text TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            offer_id INTEGER REFERENCES offers(id),
            application_letter TEXT
        )
    """)
    conn.commit()
    cur.close()

def close_connection(conn):
    conn.close()

