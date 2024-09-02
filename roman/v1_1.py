import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt

# Connect to the PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="job_app_db",         # Replace with your database name
            user="postgres",             # Replace with your PostgreSQL username
            password="password",         # Replace with your PostgreSQL password
            host="localhost"
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
        return None

# Create tables if they don't exist
def create_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                          );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS personal_info (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id),
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            cv_path TEXT,
                            skills TEXT
                          );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS offers (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id),
                            company TEXT,
                            department TEXT,
                            offer_url TEXT,
                            company_description TEXT,
                            offer_text TEXT,
                            status INTEGER,
                            response BOOLEAN
                          );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id),
                            offer_id INTEGER REFERENCES offers(id),
                            application_letter TEXT
                          );''')

        conn.commit()
        cursor.close()
        conn.close()

# Register a new user
def register_user(username, email, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                           (username, email, hashed_password))
            conn.commit()
            messagebox.showinfo("Registration", "User registered successfully.")
        except psycopg2.Error as e:
            messagebox.showerror("Registration Error", f"Failed to register user: {e}")
        cursor.close()
        conn.close()

# Login a user
def login_user(username, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            cursor.close()
            conn.close()
            return user[0]
        else:
            cursor.close()
            conn.close()
            messagebox.showerror("Login Error", "Invalid username or password.")
            return None

# Main application window
def main_menu(user_id):
    def enter_update_personal_info():
        window.destroy()
        show_personal_info(user_id)

    def add_update_job_offer():
        window.destroy()
        show_job_offer(user_id)

    def view_applications():
        window.destroy()
        show_applications(user_id)

    window = tk.Tk()
    window.title("Job Application Assistant")

    tk.Label(window, text="Main Menu").pack()

    tk.Button(window, text="Enter/Update Personal Information", command=enter_update_personal_info).pack()
    tk.Button(window, text="Add/Update Job Offer", command=add_update_job_offer).pack()
    tk.Button(window, text="View Applications", command=view_applications).pack()

    window.mainloop()

# Show personal information
def show_personal_info(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT first_name, last_name, email, cv_path, skills FROM personal_info WHERE user_id = %s', (user_id,))
        personal_info = cursor.fetchone()

        def save_personal_info():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            cv_path = cv_entry.get()
            skills = skills_entry.get()

            if personal_info:
                cursor.execute('''UPDATE personal_info
                                  SET first_name = %s, last_name = %s, email = %s, cv_path = %s, skills = %s
                                  WHERE user_id = %s''',
                               (first_name, last_name, email, cv_path, skills, user_id))
            else:
                cursor.execute('''INSERT INTO personal_info (user_id, first_name, last_name, email, cv_path, skills)
                                  VALUES (%s, %s, %s, %s, %s, %s)''',
                               (user_id, first_name, last_name, email, cv_path, skills))
            conn.commit()
            messagebox.showinfo("Success", "Personal information updated successfully.")

        def go_back():
            cursor.close()
            conn.close()
            window.destroy()
            main_menu(user_id)

        window = tk.Tk()
        window.title("Personal Information")

        tk.Label(window, text="First Name").grid(row=0, column=0)
        first_name_entry = tk.Entry(window)
        first_name_entry.grid(row=0, column=1)
        first_name_entry.insert(0, personal_info[0] if personal_info else "")

        tk.Label(window, text="Last Name").grid(row=1, column=0)
        last_name_entry = tk.Entry(window)
        last_name_entry.grid(row=1, column=1)
        last_name_entry.insert(0, personal_info[1] if personal_info else "")

        tk.Label(window, text="Email").grid(row=2, column=0)
        email_entry = tk.Entry(window)
        email_entry.grid(row=2, column=1)
        email_entry.insert(0, personal_info[2] if personal_info else "")

        tk.Label(window, text="CV Path").grid(row=3, column=0)
        cv_entry = tk.Entry(window)
        cv_entry.grid(row=3, column=1)
        cv_entry.insert(0, personal_info[3] if personal_info else "")

        tk.Label(window, text="Skills").grid(row=4, column=0)
        skills_entry = tk.Entry(window)
        skills_entry.grid(row=4, column=1)
        skills_entry.insert(0, personal_info[4] if personal_info else "")

        save_button = tk.Button(window, text="Save", command=save_personal_info)
        save_button.grid(row=5, column=1)

        back_button = tk.Button(window, text="Back", command=go_back)
        back_button.grid(row=5, column=0)

        window.bind("<Tab>", lambda event: window.focus_get().tk_focusNext().focus())
        window.bind("<Return>", lambda event: save_button.invoke())

        window.mainloop()

# Show job offer
def show_job_offer(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT company, department, offer_url, company_description, offer_text FROM offers WHERE user_id = %s', (user_id,))
        job_offer = cursor.fetchone()

        def save_job_offer():
            company = company_entry.get()
            department = department_entry.get()
            offer_url = offer_url_entry.get()
            company_description = company_description_entry.get()
            offer_text = offer_text_entry.get()

            if job_offer:
                cursor.execute('''UPDATE offers
                                  SET company = %s, department = %s, offer_url = %s, company_description = %s, offer_text = %s
                                  WHERE user_id = %s''',
                               (company, department, offer_url, company_description, offer_text, user_id))
            else:
                cursor.execute('''INSERT INTO offers (user_id, company, department, offer_url, company_description, offer_text)
                                  VALUES (%s, %s, %s, %s, %s, %s)''',
                               (user_id, company, department, offer_url, company_description, offer_text))
            conn.commit()
            messagebox.showinfo("Success", "Job offer updated successfully.")

        def go_back():
            cursor.close()
            conn.close()
            window.destroy()
            main_menu(user_id)

        window = tk.Tk()
        window.title("Job Offer")

        tk.Label(window, text="Company").grid(row=0, column=0)
        company_entry = tk.Entry(window)
        company_entry.grid(row=0, column=1)
        company_entry.insert(0, job_offer[0] if job_offer else "")

        tk.Label(window, text="Department").grid(row=1, column=0)
        department_entry = tk.Entry(window)
        department_entry.grid(row=1, column=1)
        department_entry.insert(0, job_offer[1] if job_offer else "")

        tk.Label(window, text="Offer URL").grid(row=2, column=0)
        offer_url_entry = tk.Entry(window)
        offer_url_entry.grid(row=2, column=1)
        offer_url_entry.insert(0, job_offer[2] if job_offer else "")

        tk.Label(window, text="Company Description").grid(row=3, column=0)
        company_description_entry = tk.Entry(window)
        company_description_entry.grid(row=3, column=1)
        company_description_entry.insert(0, job_offer[3] if job_offer else "")

        tk.Label(window, text="Offer Text").grid(row=4, column=0)
        offer_text_entry = tk.Entry(window)
        offer_text_entry.grid(row=4, column=1)
        offer_text_entry.insert(0, job_offer[4] if job_offer else "")

        save_button = tk.Button(window, text="Save", command=save_job_offer)
        save_button.grid(row=5, column=1)

        back_button = tk.Button(window, text="Back", command=go_back)
        back_button.grid(row=5, column=0)

        window.bind("<Tab>", lambda event: window.focus_get().tk_focusNext().focus())
        window.bind("<Return>", lambda event: save_button.invoke())

        window.mainloop()

# Show applications
def show_applications(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT a.id, o.company, a.application_letter FROM applications a JOIN offers o ON a.offer_id = o.id WHERE a.user_id = %s', (user_id,))
        applications = cursor.fetchall()

        def view_application(app_id):
            cursor.execute('SELECT application_letter FROM applications WHERE id = %s', (app_id,))
            application = cursor.fetchone()
            messagebox.showinfo("Application Details", f"Application Letter:\n{application[0]}")

        def go_back():
            cursor.close()
            conn.close()
            window.destroy()
            main_menu(user_id)

        window = tk.Tk()
        window.title("Applications")

        tk.Label(window, text="Applications").pack()

        for app in applications:
            app_frame = tk.Frame(window)
            app_frame.pack(fill="x")

            tk.Label(app_frame, text=f"Company: {app[1]}").pack(side="left")
            view_button = tk.Button(app_frame, text="View", command=lambda app_id=app[0]: view_application(app_id))
            view_button.pack(side="right")

        back_button = tk.Button(window, text="Back", command=go_back)
        back_button.pack()

        window.mainloop()

# Initialize the application
if __name__ == "__main__":
    create_tables()

    # Example user registration and login (for demonstration purposes)
    # Uncomment and modify as needed
    # register_user("testuser", "testuser@example.com", "password")
    # user_id = login_user("testuser", "password")
    # if user_id:
    #     main_menu(user_id)
