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
        CREATE TABLE IF NOT EXISTS Details (
            user_id SERIAL PRIMARY KEY REFERENCES users(id), 
            full_name VARCHAR(255),                  
            email VARCHAR(255) UNIQUE,               
            phone_number VARCHAR(20),                
            location VARCHAR(255), 
            objective TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Profiles (
            user_id SERIAL PRIMARY KEY REFERENCES users(id),              
            work_experience JSONB,                   
            education JSONB,                         
            skills TEXT[],                           
            
            achievements TEXT[],                     
            volunteer_work TEXT[],                   
            references_info JSONB                         
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Offers (
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
        CREATE TABLE IF NOT EXISTS Applications (
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