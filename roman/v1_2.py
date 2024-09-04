import tkinter as tk
from tkinter import messagebox, filedialog
import openai
import psycopg2
import hashlib
import os

# Load OpenAI API Key from a file
def load_api_key():
    api_key_path = '/home/dci-student/Desktop/aplication_project/Working-Working-API/api_key.txt'  # Replace with the full path to your API key file
    try:
        with open(api_key_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API key file not found. Please check the path and file.")
        return None

openai.api_key = load_api_key()

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="job_app_db",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="password",  # Replace with your PostgreSQL password
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        return None

conn = get_db_connection()
if not conn:
    raise SystemExit("Failed to connect to the database. Please check your credentials.")

cur = conn.cursor()

# Database schema creation
def create_tables():
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

# Call the function to create tables on initialization
create_tables()

# User authentication (register/login)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    hashed_password = hash_password(password)
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, hashed_password))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False

def login_user(username, password):
    hashed_password = hash_password(password)
    cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", 
                (username, hashed_password))
    user = cur.fetchone()
    return user[0] if user else None

# Personal data collection
def collect_personal_data(user_id, first_name, last_name, email, cv_path, skills):
    cur.execute("INSERT INTO personal_info (first_name, last_name, email, cv_path, user_id) VALUES (%s, %s, %s, %s, %s)", 
                (first_name, last_name, email, cv_path, user_id))
    for skill in skills.split(','):
        cur.execute("INSERT INTO skills (skill, user_id) VALUES (%s, %s)", (skill.strip(), user_id))
    conn.commit()

# Job offer management
def add_job_offer(user_id, company, department, offer_url, company_description, offer_text):
    cur.execute("""
    INSERT INTO offers (company, department, offer_url, company_description, offer_text, status, response, user_id)
    VALUES (%s, %s, %s, %s, %s, 0, FALSE, %s)
    """, (company, department, offer_url, company_description, offer_text, user_id))
    conn.commit()

# Application letter generation
def generate_application_letter(skills, offer_text):
    if openai.api_key is None:
        return "OpenAI API key not set."
    
    prompt = f"Based on the following skills: {skills}, write an application letter for this job offer: {offer_text}"
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Error generating application letter."

def save_application_letter(application_id, letter):
    cur.execute("INSERT INTO application_letters (application_id, letter) VALUES (%s, %s)", 
                (application_id, letter))
    conn.commit()

# Application tracking
def track_application(offer_id, user_id):
    cur.execute("INSERT INTO applications (offer_id, user_id) VALUES (%s, %s)", 
                (offer_id, user_id))
    conn.commit()

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Job Application Assistant")

    # Register/Login
    def show_login():
        login_frame.pack(fill="both", expand=True)
        register_frame.pack_forget()

    def show_register():
        register_frame.pack(fill="both", expand=True)
        login_frame.pack_forget()

    def login():
        username = login_username_entry.get()
        password = login_password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            login_frame.pack_forget()
            show_personal_info(user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register():
        username = register_username_entry.get()
        email = register_email_entry.get()
        password = register_password_entry.get()
        if register_user(username, email, password):
            messagebox.showinfo("Registration Successful", "You can now log in.")
            show_login()
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    # Personal Info
    def show_personal_info(user_id):
        personal_info_frame.pack(fill="both", expand=True)
        
        def save_personal_info():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = personal_email_entry.get()
            cv_path = filedialog.askopenfilename()
            skills = skills_entry.get()
            collect_personal_data(user_id, first_name, last_name, email, cv_path, skills)
            show_job_offer_section(user_id)
        
        tk.Label(personal_info_frame, text="First Name").grid(row=0, column=0)
        first_name_entry = tk.Entry(personal_info_frame)
        first_name_entry.grid(row=0, column=1)

        tk.Label(personal_info_frame, text="Last Name").grid(row=1, column=0)
        last_name_entry = tk.Entry(personal_info_frame)
        last_name_entry.grid(row=1, column=1)

        tk.Label(personal_info_frame, text="Email").grid(row=2, column=0)
        personal_email_entry = tk.Entry(personal_info_frame)
        personal_email_entry.grid(row=2, column=1)

        tk.Label(personal_info_frame, text="Skills (comma-separated)").grid(row=3, column=0)
        skills_entry = tk.Entry(personal_info_frame)
        skills_entry.grid(row=3, column=1)

        tk.Button(personal_info_frame, text="Save", command=save_personal_info).grid(row=4, column=0, columnspan=2)

    # Job Offer Section
    def show_job_offer_section(user_id):
        job_offer_frame.pack(fill="both", expand=True)

        def save_job_offer():
            company = company_entry.get()
            department = department_entry.get()
            offer_url = offer_url_entry.get()
            company_description = company_description_text.get("1.0", tk.END).strip()
            offer_text = offer_text_text.get("1.0", tk.END).strip()
            add_job_offer(user_id, company, department, offer_url, company_description, offer_text)
            generate_and_save_application(user_id, company_description, offer_text)

        def generate_and_save_application(user_id, company_description, offer_text):
            skills = get_skills(user_id)
            letter = generate_application_letter(skills, offer_text)
            cur.execute("SELECT id FROM offers WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
            offer_id = cur.fetchone()[0]
            track_application(offer_id, user_id)
            cur.execute("SELECT id FROM applications WHERE offer_id = %s AND user_id = %s", (offer_id, user_id))
            application_id = cur.fetchone()[0]
            save_application_letter(application_id, letter)
            messagebox.showinfo("Application Generated", "Your application letter has been generated and saved.")

        def get_skills(user_id):
            cur.execute("SELECT skill FROM skills WHERE user_id = %s", (user_id,))
            skills = [skill[0] for skill in cur.fetchall()]
            return ', '.join(skills)

        tk.Label(job_offer_frame, text="Company").grid(row=0, column=0)
        company_entry = tk.Entry(job_offer_frame)
        company_entry.grid(row=0, column=1)

        tk.Label(job_offer_frame, text="Department").grid(row=1, column=0)
        department_entry = tk.Entry(job_offer_frame)
        department_entry.grid(row=1, column=1)

        tk.Label(job_offer_frame, text="Offer URL").grid(row=2, column=0)
        offer_url_entry = tk.Entry(job_offer_frame)
        offer_url_entry.grid(row=2, column=1)

        tk.Label(job_offer_frame, text="Company Description").grid(row=3, column=0)
        company_description_text = tk.Text(job_offer_frame, height=4, width=30)
        company_description_text.grid(row=3, column=1)

        tk.Label(job_offer_frame, text="Offer Text").grid(row=4, column=0)
        offer_text_text = tk.Text(job_offer_frame, height=4, width=30)
        offer_text_text.grid(row=4, column=1)

        tk.Button(job_offer_frame, text="Save Offer", command=save_job_offer).grid(row=5, column=0, columnspan=2)

    # Frames
    login_frame = tk.Frame(root)
    register_frame = tk.Frame(root)
    personal_info_frame = tk.Frame(root)
    job_offer_frame = tk.Frame(root)

    # Login Frame
    tk.Label(login_frame, text="Username").grid(row=0, column=0)
    login_username_entry = tk.Entry(login_frame)
    login_username_entry.grid(row=0, column=1)

    tk.Label(login_frame, text="Password").grid(row=1, column=0)
    login_password_entry = tk.Entry(login_frame, show='*')
    login_password_entry.grid(row=1, column=1)

    tk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2)
    tk.Button(login_frame, text="Register", command=show_register).grid(row=3, column=0, columnspan=2)

    # Register Frame
    tk.Label(register_frame, text="Username").grid(row=0, column=0)
    register_username_entry = tk.Entry(register_frame)
    register_username_entry.grid(row=0, column=1)

    tk.Label(register_frame, text="Email").grid(row=1, column=0)
    register_email_entry = tk.Entry(register_frame)
    register_email_entry.grid(row=1, column=1)

    tk.Label(register_frame, text="Password").grid(row=2, column=0)
    register_password_entry = tk.Entry(register_frame, show='*')
    register_password_entry.grid(row=2, column=1)

    tk.Button(register_frame, text="Register", command=register).grid(row=3, column=0, columnspan=2)
    tk.Button(register_frame, text="Back to Login", command=show_login).grid(row=4, column=0, columnspan=2)

    # Initial Frame
    login_frame.pack(fill="both", expand=True)

    root.mainloop()

# Create tables and launch the GUI
create_tables()
create_gui()

# Close the database connection when done
cur.close()
conn.close()
