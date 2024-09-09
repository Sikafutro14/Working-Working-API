import tkinter as tk
from tkinter import messagebox, filedialog
import openai
import psycopg2
from psycopg2 import sql, extras
import hashlib
import os
import sys

# Function to load the API key from the parent directory
def load_api_key():
    try:
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        api_key_path = os.path.join(parent_directory, 'api_key.txt')
        with open(api_key_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        messagebox.showerror("API Key Error", f"Failed to load API key: {e}")
        sys.exit(1)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to connect to the database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="job_app_db",         # Replace with your database name
            user="postgres",         # Replace with your PostgreSQL username
            password="password", # Replace with your PostgreSQL password
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        messagebox.showerror("Database Connection Error", f"Failed to connect to the database.\nError: {e}")
        sys.exit(1)

# Function to create necessary tables
def create_tables(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS personal_info (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100),
                cv_path VARCHAR(255),
                user_id INTEGER REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS skills (
                id SERIAL PRIMARY KEY,
                skill TEXT NOT NULL,
                user_id INTEGER REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                company VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                offer_url TEXT,
                company_description TEXT,
                offer_text TEXT,
                status INT,
                response BOOLEAN,
                user_id INTEGER REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                offer_id INTEGER REFERENCES offers(id),
                user_id INTEGER REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS application_letters (
                id SERIAL PRIMARY KEY,
                application_id INTEGER REFERENCES applications(id),
                letter TEXT NOT NULL
            );
            """)
            conn.commit()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to create tables.\nError: {e}")
        conn.rollback()
        sys.exit(1)

# Function to check if any users exist
def check_for_users(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to check users.\nError: {e}")
        return False

# Function to register a new user
def register_user(conn, username, email, password, first_name, last_name):
    hashed_password = hash_password(password)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (username, email, hashed_password))
            user_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO personal_info (first_name, last_name, email, user_id)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, email, user_id))

            conn.commit()
            return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        messagebox.showerror("Registration Error", "Username already exists. Please choose a different username.")
        return None
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Registration Error", f"Failed to register user.\nError: {e}")
        return None

# Function to log in a user
def login_user(conn, username, password):
    hashed_password = hash_password(password)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM users WHERE username = %s AND password = %s
            """, (username, hashed_password))
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                return None
    except Exception as e:
        messagebox.showerror("Login Error", f"Failed to log in.\nError: {e}")
        return None

# Function to collect and save personal data
def collect_personal_data(conn, user_id, first_name, last_name, email, cv_path, skills):
    try:
        with conn.cursor() as cur:
            # Update personal_info
            cur.execute("""
                UPDATE personal_info
                SET first_name = %s, last_name = %s, email = %s, cv_path = %s
                WHERE user_id = %s
            """, (first_name, last_name, email, cv_path, user_id))

            # Clear existing skills
            cur.execute("DELETE FROM skills WHERE user_id = %s", (user_id,))

            # Insert new skills
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            extras.execute_values(cur, """
                INSERT INTO skills (skill, user_id) VALUES %s
            """, [(skill, user_id) for skill in skills_list])

            conn.commit()
            messagebox.showinfo("Success", "Personal information saved successfully.")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to save personal information.\nError: {e}")

# Function to add a job offer
def add_job_offer(conn, user_id, company, department, offer_url, company_description, offer_text):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO offers (company, department, offer_url, company_description, offer_text, status, response, user_id)
                VALUES (%s, %s, %s, %s, %s, 0, FALSE, %s)
                RETURNING id
            """, (company, department, offer_url, company_description, offer_text, user_id))
            offer_id = cur.fetchone()[0]
            conn.commit()
            messagebox.showinfo("Success", "Job offer added successfully.")
            return offer_id
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to add job offer.\nError: {e}")
        return None

# Function to generate application letter using OpenAI
def generate_application_letter(skills, offer_text):
    try:
        prompt = f"Based on the following skills: {skills}, write a professional application letter for this job offer:\n\n{offer_text}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        letter = response.choices[0].text.strip()
        return letter
    except Exception as e:
        messagebox.showerror("OpenAI Error", f"Failed to generate application letter.\nError: {e}")
        return None

# Function to save application and generated letter
def save_application(conn, user_id, offer_id, letter):
    try:
        with conn.cursor() as cur:
            # Insert into applications
            cur.execute("""
                INSERT INTO applications (offer_id, user_id)
                VALUES (%s, %s)
                RETURNING id
            """, (offer_id, user_id))
            application_id = cur.fetchone()[0]

            # Insert into application_letters
            cur.execute("""
                INSERT INTO application_letters (application_id, letter)
                VALUES (%s, %s)
            """, (application_id, letter))

            conn.commit()
            messagebox.showinfo("Success", "Application letter generated and saved successfully.")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to save application letter.\nError: {e}")

# Main Application Class
class JobAppAssistant:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.user_id = None

        self.root.title("Job Application Assistant")
        self.root.geometry("600x500")

        # Initialize frames
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.personal_info_frame = tk.Frame(self.root)
        self.job_offer_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)

        # Build all frames
        self.build_login_frame()
        self.build_register_frame()
        self.build_personal_info_frame()
        self.build_job_offer_frame()
        self.build_main_frame()

    def show_frame(self, frame):
        frame.tkraise()

    def build_login_frame(self):
        frame = self.login_frame
        frame.grid(row=0, column=0, sticky='nsew')

        tk.Label(frame, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(frame, text="Username:").pack(pady=5)
        self.login_username_entry = tk.Entry(frame)
        self.login_username_entry.pack()

        tk.Label(frame, text="Password:").pack(pady=5)
        self.login_password_entry = tk.Entry(frame, show='*')
        self.login_password_entry.pack()

        tk.Button(frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(frame, text="Register", command=lambda: self.show_frame(self.register_frame)).pack()

    def build_register_frame(self):
        frame = self.register_frame
        frame.grid(row=0, column=0, sticky='nsew')

        tk.Label(frame, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(frame, text="Username:").pack(pady=5)
        self.reg_username_entry = tk.Entry(frame)
        self.reg_username_entry.pack()

        tk.Label(frame, text="Email:").pack(pady=5)
        self.reg_email_entry = tk.Entry(frame)
        self.reg_email_entry.pack()

        tk.Label(frame, text="Password:").pack(pady=5)
        self.reg_password_entry = tk.Entry(frame, show='*')
        self.reg_password_entry.pack()

        tk.Label(frame, text="First Name:").pack(pady=5)
        self.reg_first_name_entry = tk.Entry(frame)
        self.reg_first_name_entry.pack()

        tk.Label(frame, text="Last Name:").pack(pady=5)
        self.reg_last_name_entry = tk.Entry(frame)
        self.reg_last_name_entry.pack()

        tk.Button(frame, text="Register", command=self.register).pack(pady=10)
        tk.Button(frame, text="Back to Login", command=lambda: self.show_frame(self.login_frame)).pack()

    def build_personal_info_frame(self):
        frame = self.personal_info_frame
        frame.grid(row=0, column=0, sticky='nsew')

        tk.Label(frame, text="Personal Information", font=("Arial", 16)).pack(pady=10)

        tk.Label(frame, text="First Name:").pack(pady=5)
        self.pi_first_name_entry = tk.Entry(frame)
        self.pi_first_name_entry.pack()

        tk.Label(frame, text="Last Name:").pack(pady=5)
        self.pi_last_name_entry = tk.Entry(frame)
        self.pi_last_name_entry.pack()

        tk.Label(frame, text="Email:").pack(pady=5)
        self.pi_email_entry = tk.Entry(frame)
        self.pi_email_entry.pack()

        tk.Label(frame, text="CV Path:").pack(pady=5)
        self.pi_cv_path_entry = tk.Entry(frame)
        self.pi_cv_path_entry.pack()
        tk.Button(frame, text="Browse", command=self.browse_cv).pack(pady=5)

        tk.Label(frame, text="Skills (comma-separated):").pack(pady=5)
        self.pi_skills_entry = tk.Entry(frame)
        self.pi_skills_entry.pack()

        tk.Button(frame, text="Save Personal Info", command=self.save_personal_info).pack(pady=10)

    def build_job_offer_frame(self):
        frame = self.job_offer_frame
        frame.grid(row=0, column=0, sticky='nsew')

        tk.Label(frame, text="Add Job Offer", font=("Arial", 16)).pack(pady=10)

        tk.Label(frame, text="Company:").pack(pady=5)
        self.offer_company_entry = tk.Entry(frame)
        self.offer_company_entry.pack()

        tk.Label(frame, text="Department:").pack(pady=5)
        self.offer_department_entry = tk.Entry(frame)
        self.offer_department_entry.pack()

        tk.Label(frame, text="Offer URL:").pack(pady=5)
        self.offer_url_entry = tk.Entry(frame)
        self.offer_url_entry.pack()

        tk.Label(frame, text="Company Description:").pack(pady=5)
        self.offer_company_desc_text = tk.Text(frame, height=4, width=50)
        self.offer_company_desc_text.pack()

        tk.Label(frame, text="Offer Text:").pack(pady=5)
        self.offer_text_text = tk.Text(frame, height=4, width=50)
        self.offer_text_text.pack()

        tk.Button(frame, text="Save Offer and Generate Application", command=self.save_offer_and_generate).pack(pady=10)
        tk.Button(frame, text="Back to Main", command=lambda: self.show_frame(self.main_frame)).pack()

    def build_main_frame(self):
        frame = self.main_frame
        frame.grid(row=0, column=0, sticky='nsew')

        tk.Label(frame, text="Job Application Assistant", font=("Arial", 16)).pack(pady=10)

        tk.Button(frame, text="Enter Personal Information", width=30, command=lambda: self.show_frame(self.personal_info_frame)).pack(pady=10)
        tk.Button(frame, text="Add Job Offer", width=30, command=lambda: self.show_frame(self.job_offer_frame)).pack(pady=10)
        tk.Button(frame, text="Logout", width=30, command=self.logout).pack(pady=10)

    def browse_cv(self):
        file_path = filedialog.askopenfilename(title="Select CV", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if file_path:
            self.pi_cv_path_entry.delete(0, tk.END)
            self.pi_cv_path_entry.insert(0, file_path)

    def login(self):
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        user_id = login_user(self.conn, username, password)
        if user_id:
            self.user_id = user_id
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.show_frame(self.main_frame)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.reg_username_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        first_name = self.reg_first_name_entry.get().strip()
        last_name = self.reg_last_name_entry.get().strip()

        if not all([username, email, password, first_name, last_name]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        user_id = register_user(self.conn, username, email, password, first_name, last_name)
        if user_id:
            messagebox.showinfo("Registration Successful", "You have registered successfully! Please log in.")
            self.show_frame(self.login_frame)

    def save_personal_info(self):
        first_name = self.pi_first_name_entry.get().strip()
        last_name = self.pi_last_name_entry.get().strip()
        email = self.pi_email_entry.get().strip()
        cv_path = self.pi_cv_path_entry.get().strip()
        skills = self.pi_skills_entry.get().strip()

        if not all([first_name, last_name, email, skills]):
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        collect_personal_data(self.conn, self.user_id, first_name, last_name, email, cv_path, skills)

    def save_offer_and_generate(self):
        company = self.offer_company_entry.get().strip()
        department = self.offer_department_entry.get().strip()
        offer_url = self.offer_url_entry.get().strip()
        company_description = self.offer_company_desc_text.get("1.0", tk.END).strip()
        offer_text = self.offer_text_text.get("1.0", tk.END).strip()

        if not company or not offer_text:
            messagebox.showwarning("Input Error", "Please fill in all required fields (Company and Offer Text).")
            return

        offer_id = add_job_offer(self.conn, self.user_id, company, department, offer_url, company_description, offer_text)
        if offer_id:
            # Fetch user skills
            skills = self.get_user_skills()
            if not skills:
                messagebox.showwarning("Skills Missing", "No skills found. Please enter your skills in Personal Information.")
                return

            # Generate application letter
            letter = generate_application_letter(skills, offer_text)
            if letter:
                # Save application and letter
                save_application(self.conn, self.user_id, offer_id, letter)

    def get_user_skills(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT skill FROM skills WHERE user_id = %s", (self.user_id,))
                skills = [skill[0] for skill in cur.fetchall()]
                return ', '.join(skills)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve skills.\nError: {e}")
            return ''

    def logout(self):
        self.user_id = None
        messagebox.showinfo("Logged Out", "You have been logged out.")
        self.show_frame(self.login_frame)

# Function to initialize and run the application
def main():
    # Initialize Tkinter
    root = tk.Tk()

    # Load API key
    openai.api_key = load_api_key()

    # Connect to the database
    conn = connect_to_db()

    # Create tables if they don't exist
    create_tables(conn)

    # Check if any users exist
    if not check_for_users(conn):
        # No users found, open registration window
        app = JobAppAssistant(root, conn)
        app.show_frame(app.register_frame)
    else:
        # Users exist, open login window
        app = JobAppAssistant(root, conn)
        app.show_frame(app.login_frame)

    # Start the Tkinter main loop
    root.mainloop()

    # Close the database connection when the application is closed
    conn.close()

if __name__ == "__main__":
    main()
