import tkinter as tk
from tkinter import messagebox, filedialog
import psycopg2
from psycopg2 import extras
import hashlib
import os
import sys
from ai_module import generate_application_letter

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to connect to the database
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

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_window()

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=50)

        tk.Label(login_frame, text="Login", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

        tk.Label(login_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=1, column=1, padx=10, pady=5)
        username_entry.focus()

        tk.Label(login_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        def on_enter(event=None):
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return

            self.user_id = login_user(self.conn, username, password)
            if self.user_id:
                self.show_main_menu()
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")

        tk.Button(login_frame, text="Login", command=on_enter).grid(row=3, columnspan=2, pady=10)
        self.root.bind('<Return>', on_enter)

        tk.Label(login_frame, text="Don't have an account?").grid(row=4, column=0, padx=10, pady=5)
        tk.Button(login_frame, text="Register", command=self.show_registration_screen).grid(row=4, column=1, padx=10, pady=5)

    def show_registration_screen(self):
        self.clear_window()

        reg_frame = tk.Frame(self.root)
        reg_frame.pack(pady=50)

        tk.Label(reg_frame, text="Register", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

        tk.Label(reg_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        username_entry = tk.Entry(reg_frame)
        username_entry.grid(row=1, column=1, padx=10, pady=5)
        username_entry.focus()

        tk.Label(reg_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        email_entry = tk.Entry(reg_frame)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(reg_frame, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        password_entry = tk.Entry(reg_frame, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(reg_frame, text="Confirm Password:").grid(row=4, column=0, padx=10, pady=5)
        confirm_password_entry = tk.Entry(reg_frame, show="*")
        confirm_password_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(reg_frame, text="First Name:").grid(row=5, column=0, padx=10, pady=5)
        first_name_entry = tk.Entry(reg_frame)
        first_name_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(reg_frame, text="Last Name:").grid(row=6, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(reg_frame)
        last_name_entry.grid(row=6, column=1, padx=10, pady=5)

        def on_register():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()

            if not username or not email or not password or not confirm_password or not first_name or not last_name:
                messagebox.showerror("Error", "All fields are required.")
                return
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            user_id = register_user(self.conn, username, email, password, first_name, last_name)
            if user_id:
                self.user_id = user_id
                self.show_main_menu()

        tk.Button(reg_frame, text="Register", command=on_register).grid(row=7, columnspan=2, pady=10)

        tk.Button(reg_frame, text="Back to Login", command=self.show_login_screen).grid(row=8, columnspan=2, pady=10)

    def show_main_menu(self):
        self.clear_window()

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=50)

        tk.Label(main_frame, text="Main Menu", font=("Arial", 18)).pack(pady=10)

        tk.Button(main_frame, text="Update Personal Information", command=self.show_personal_info_screen).pack(pady=10)
        tk.Button(main_frame, text="Add Job Offer", command=self.show_job_offer_screen).pack(pady=10)
        tk.Button(main_frame, text="Generate Application Letter", command=self.show_application_letter_screen).pack(pady=10)
        tk.Button(main_frame, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_personal_info_screen(self):
        self.clear_window()

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=50)

        tk.Label(info_frame, text="Update Personal Information", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="First Name:").grid(row=1, column=0, padx=10, pady=5)
        first_name_entry = tk.Entry(info_frame)
        first_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(info_frame)
        last_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Email:").grid(row=3, column=0, padx=10, pady=5)
        email_entry = tk.Entry(info_frame)
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="CV Path:").grid(row=4, column=0, padx=10, pady=5)
        cv_entry = tk.Entry(info_frame)
        cv_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Button(info_frame, text="Browse", command=lambda: self.browse_cv(cv_entry)).grid(row=4, column=2, padx=10, pady=5)

        tk.Label(info_frame, text="Skills (comma-separated):").grid(row=5, column=0, padx=10, pady=5)
        skills_entry = tk.Entry(info_frame)
        skills_entry.grid(row=5, column=1, padx=10, pady=5)

        def on_save():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            email = email_entry.get().strip()
            cv_path = cv_entry.get().strip()
            skills = skills_entry.get().strip()

            if not first_name or not last_name or not email:
                messagebox.showerror("Error", "Please fill out all required fields.")
                return

            collect_personal_data(self.conn, self.user_id, first_name, last_name, email, cv_path, skills)

        tk.Button(info_frame, text="Save", command=on_save).grid(row=6, columnspan=3, pady=10)
        tk.Button(info_frame, text="Back", command=self.show_main_menu).grid(row=7, columnspan=3, pady=10)

    def browse_cv(self, entry):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def show_job_offer_screen(self):
        self.clear_window()

        offer_frame = tk.Frame(self.root)
        offer_frame.pack(pady=50)

        tk.Label(offer_frame, text="Add Job Offer", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

        tk.Label(offer_frame, text="Company:").grid(row=1, column=0, padx=10, pady=5)
        company_entry = tk.Entry(offer_frame)
        company_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(offer_frame, text="Department:").grid(row=2, column=0, padx=10, pady=5)
        department_entry = tk.Entry(offer_frame)
        department_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(offer_frame, text="Offer URL:").grid(row=3, column=0, padx=10, pady=5)
        offer_url_entry = tk.Entry(offer_frame)
        offer_url_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(offer_frame, text="Company Description:").grid(row=4, column=0, padx=10, pady=5)
        company_description_entry = tk.Entry(offer_frame)
        company_description_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(offer_frame, text="Offer Text:").grid(row=5, column=0, padx=10, pady=5)
        offer_text_entry = tk.Entry(offer_frame)
        offer_text_entry.grid(row=5, column=1, padx=10, pady=5)

        def on_add_offer():
            company = company_entry.get().strip()
            department = department_entry.get().strip()
            offer_url = offer_url_entry.get().strip()
            company_description = company_description_entry.get().strip()
            offer_text = offer_text_entry.get().strip()

            if not company or not department or not offer_url or not company_description or not offer_text:
                messagebox.showerror("Error", "Please fill out all fields.")
                return

            offer_id = add_job_offer(self.conn, self.user_id, company, department, offer_url, company_description, offer_text)
            if offer_id:
                self.show_main_menu()

        tk.Button(offer_frame, text="Add Offer", command=on_add_offer).grid(row=6, columnspan=2, pady=10)
        tk.Button(offer_frame, text="Back", command=self.show_main_menu).grid(row=7, columnspan=2, pady=10)

    def show_application_letter_screen(self):
        self.clear_window()

        letter_frame = tk.Frame(self.root)
        letter_frame.pack(pady=50)

        tk.Label(letter_frame, text="Generate Application Letter", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

        tk.Label(letter_frame, text="Job Offer ID:").grid(row=1, column=0, padx=10, pady=5)
        offer_id_entry = tk.Entry(letter_frame)
        offer_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(letter_frame, text="Personal Statement:").grid(row=2, column=0, padx=10, pady=5)
        personal_statement_entry = tk.Entry(letter_frame)
        personal_statement_entry.grid(row=2, column=1, padx=10, pady=5)

        def on_generate_letter():
            offer_id = offer_id_entry.get().strip()
            personal_statement = personal_statement_entry.get().strip()

            if not offer_id or not personal_statement:
                messagebox.showerror("Error", "Please fill out all fields.")
                return

            letter = generate_application_letter(self.conn, self.user_id, offer_id, personal_statement)
            if letter:
                self.show_main_menu()
                messagebox.showinfo("Success", "Application letter generated successfully!")

        tk.Button(letter_frame, text="Generate Letter", command=on_generate_letter).grid(row=3, columnspan=2, pady=10)
        tk.Button(letter_frame, text="Back", command=self.show_main_menu).grid(row=4, columnspan=2, pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
