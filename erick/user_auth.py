import psycopg2
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(conn, username, email, password, first_name, last_name):
    try:
        cur = conn.cursor()
        password_hash = hash_password(password)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (username, email, password_hash, first_name, last_name))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return user_id
    except Exception as e:
        print(f"Error registering user: {e}")
        return None
    
def login_user(conn, username, password):
    try:
        cur = conn.cursor()
        password_hash = hash_password(password)
        cur.execute("""
            SELECT id FROM users WHERE username = %s AND password_hash = %s
        """, (username, password_hash))
        user = cur.fetchone()
        cur.close()
        if user:
            return user[0]
        else:
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def verify_user(username, password):
    try:
        with psycopg2.connect(
            dbname="job_app_db", 
            user="postgres", 
            password="password", 
            host="localhost", 
            port="5432"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT password FROM users WHERE username = %s
                """, (username,))
                
                user = cur.fetchone()

                if user:
                    stored_password = user[0]
                    if password == stored_password:
                        return True
                    else:
                        print("Password does not match.")
                        return False
                else:
                    print("User not found.")
                    return False

    except Exception as e:
        print(f"An error occurred during user verification: {e}")
        return False