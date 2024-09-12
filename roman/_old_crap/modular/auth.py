import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn, username, email, password, first_name, last_name):
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
