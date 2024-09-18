import psycopg2
from psycopg2 import sql
from user_auth import get_db_connection

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personal_info (
            user_id INTEGER PRIMARY KEY REFERENCES users(id), 
            first_name VARCHAR(255),   
            last_name VARCHAR(255),               
            email VARCHAR(255) UNIQUE,               
            background TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            position VARCHAR(255),
            company VARCHAR(255),
            about TEXT,
            offer TEXT,
            url VARCHAR(255),
            status INTEGER,
            response BOOLEAN
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

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        create_tables(conn)
        close_connection(conn)