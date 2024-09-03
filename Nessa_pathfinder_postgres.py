import random
import datetime
import os
import psycopg2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai    
import tkinter as tk
from tkinter import messagebox
import requests



def create_db():
    # Connect to the database (creates it if it doesn't exist)
    conn = psycopg2.connect(
        dbname = 'pathfinder',
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = '5432'
        )
    conn.autocommit = True

    cursor = conn.cursor()


    # Create the tables
    cursor.execute('''
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    resume TEXT
);
''')

    cursor.execute('''
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    company VARCHAR(100),
    position VARCHAR(100),
    status VARCHAR(50),
    application_date DATE
);

''')
    
    
    
app = Flask(__name__)

# Configure your database URI
#app.config[' SQLAlchemy_DATABASE_URI'] = 'postgresql://username:password@localhost/pathfinder'
#app.config[' SQLAlchemy_TRACK_MODIFICATIONS'] = False

app.config['SQLAlchemy_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'

db = SQLAlchemy(app)

#database models
class user(db.Model):
    id = db.Column(db.interger, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    resume = db.Column(db.Text)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    status = db.Column(db.String(50))
    application_date = db.Column(db.Date)

# Initialize database
with app.app_context():
    db.create_all()
    
    

# Set your OpenAI API key
openai.api_key = "API key:  )"

# API route to create a job application
@app.route('/create_application', methods=['POST'])
def create_application():
    data = request.json
    new_application = JobApplication(
        user_id=data['user_id'],
        company=data['company'],
        position=data['position'],
        status=data['status'],
        application_date=data['application_date']
    )
    db.session.add(new_application)
    db.session.commit()
    return jsonify({'message': 'Application created successfully'})


# API route to use OpenAI for resume enhancement
@app.route('/enhance_resume', methods=['POST'])
def enhance_resume():
    data = request.json
    prompt = f"Enhance the following resume: {data['resume']}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    enhanced_resume = response.choices[0].text.strip()
    return jsonify({'enhanced_resume': enhanced_resume})



if __name__ == '__main__':
    app.run(debug=True)


class PathFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Finder - Job Application Tracker")

        # Entry widgets
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, padx=20)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.grid(row=1, column=1, padx=20)
        self.resume_entry = tk.Text(root, width=40, height=10)
        self.resume_entry.grid(row=2, column=1, padx=20, pady=10)

        # Labels
        tk.Label(root, text="Name:").grid(row=0, column=0, pady=5)
        tk.Label(root, text="Email:").grid(row=1, column=0, pady=5)
        tk.Label(root, text="Resume:").grid(row=2, column=0, pady=5)

        # Buttons
        tk.Button(root, text="Enhance Resume", command=self.enhance_resume).grid(row=3, column=1, pady=5)
        tk.Button(root, text="Submit Application", command=self.submit_application).grid(row=4, column=1, pady=5)

    def enhance_resume(self):
        resume_text = self.resume_entry.get("1.0", tk.END)
        response = requests.post('http://127.0.0.1:5000/enhance_resume', json={'resume': resume_text})
        if response.status_code == 200:
            enhanced_resume = response.json()['enhanced_resume']
            self.resume_entry.delete("1.0", tk.END)
            self.resume_entry.insert(tk.END, enhanced_resume)
        else:
            messagebox.showerror("Error", "Failed to enhance resume.")

    def submit_application(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        resume = self.resume_entry.get("1.0", tk.END)
        
        # Normally you'd save these details in the database
        # For now, let's just print them as a placeholder
        print(f"Name: {name}, Email: {email}, Resume: {resume}")

# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PathFinderApp(root)
    root.mainloop()
  
    import tkinter as tk
from tkinter import messagebox
import requests

class PathFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Finder - Job Application Tracker")

        # Entry widgets
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, padx=20)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.grid(row=1, column=1, padx=20)
        self.resume_entry = tk.Text(root, width=40, height=10)
        self.resume_entry.grid(row=2, column=1, padx=20, pady=10)

        # Labels
        tk.Label(root, text="Name:").grid(row=0, column=0, pady=5)
        tk.Label(root, text="Email:").grid(row=1, column=0, pady=5)
        tk.Label(root, text="Resume:").grid(row=2, column=0, pady=5)

        # Buttons
        tk.Button(root, text="Enhance Resume", command=self.enhance_resume).grid(row=3, column=1, pady=5)
        tk.Button(root, text="Submit Application", command=self.submit_application).grid(row=4, column=1, pady=5)

    def enhance_resume(self):
        resume_text = self.resume_entry.get("1.0", tk.END)
        response = requests.post('http://127.0.0.1:5000/enhance_resume', json={'resume': resume_text})
        if response.status_code == 200:
            enhanced_resume = response.json()['enhanced_resume']
            self.resume_entry.delete("1.0", tk.END)
            self.resume_entry.insert(tk.END, enhanced_resume)
        else:
            messagebox.showerror("Error", "Failed to enhance resume.")

    def submit_application(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        resume = self.resume_entry.get("1.0", tk.END)
        
        # Normally you'd save these details in the database
        # For now, let's just print them as a placeholder
        print(f"Name: {name}, Email: {email}, Resume: {resume}")

# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PathFinderApp(root)
    root.mainloop()
