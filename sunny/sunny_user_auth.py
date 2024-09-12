import psycopg2
import bcrypt

# Database connection
def get_db_connection():
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

# Register function
def register(username, email, password):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email)) 

            if cursor.fetchone():
                return "Username or email already exists."

            # Generate a secure salt and hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

            # Insert the new user with hashed password
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )

            conn.commit()
            return "User registered successfully!"

    except psycopg2.OperationalError as e:
        return f"Database connection error: {str(e)}"
    except Exception as e:
        return str(e)

def login(username, password):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                return "User not found.", None

            stored_password = user[1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return "Login successful!", user[0]
            else:
                return "Incorrect password.", None

    except psycopg2.OperationalError as e:
        return f"Database connection error: {str(e)}", None
    except Exception as e:
        return str(e), None
    

def login_user(self):
    username = self.username_entry.get()
    password = self.password_entry.get()

    if not username or not password:
        self.show_error_message("Please enter both username and password.")
        return

    # Call the login function from sunny_user_auth.py
    message, user_id = login(username, password)

    if user_id:
        self.show_info_message(f"Login successful! User ID: {user_id}")
        self.user_id_entry.delete(0, "end")
        self.user_id_entry.insert(0, user_id)  # Auto-populate the user ID after login
    else:
        self.show_error_message(message)
