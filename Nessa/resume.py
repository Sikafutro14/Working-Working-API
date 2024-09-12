import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import psycopg2

class ResumeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Information")

        # Personal Information
        self.create_personal_info_widgets()
        # Objective
        self.create_objective_widgets()
        # Work Experience
        self.create_work_experience_widgets()
        # Education
        self.create_education_widgets()
        # Skills
        self.create_skills_widgets()
        # Achievements
        self.create_achievements_widgets()
        # Volunteer Work
        self.create_volunteer_work_widgets()
        # References
        self.create_references_widgets()
        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def create_personal_info_widgets(self):
        tk.Label(self.root, text="Full Name:").pack(pady=5)
        self.full_name_entry = tk.Entry(self.root)
        self.full_name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Phone Number:").pack(pady=5)
        self.phone_number_entry = tk.Entry(self.root)
        self.phone_number_entry.pack(pady=5)

        tk.Label(self.root, text="Location:").pack(pady=5)
        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack(pady=5)

    def create_objective_widgets(self):
        tk.Label(self.root, text="Objective:").pack(pady=5)
        self.objective_text = scrolledtext.ScrolledText(self.root, height=5, width=40)
        self.objective_text.pack(pady=5)

    def create_work_experience_widgets(self):
        self.work_experience_frame = tk.LabelFrame(self.root, text="Work Experience")
        self.work_experience_frame.pack(pady=10, padx=10, fill=tk.X)

        self.work_experience_entries = []

        def add_work_experience():
            frame = tk.Frame(self.work_experience_frame)
            frame.pack(pady=5, fill=tk.X)

            tk.Label(frame, text="Job Title:").pack(side=tk.LEFT, padx=5)
            title_entry = tk.Entry(frame, width=20)
            title_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Company:").pack(side=tk.LEFT, padx=5)
            company_entry = tk.Entry(frame, width=20)
            company_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
            start_date_entry = tk.Entry(frame, width=10)
            start_date_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="End Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
            end_date_entry = tk.Entry(frame, width=10)
            end_date_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Responsibilities:").pack(side=tk.LEFT, padx=5)
            responsibilities_entry = tk.Entry(frame, width=40)
            responsibilities_entry.pack(side=tk.LEFT, padx=5)

            self.work_experience_entries.append({
                'frame': frame,
                'title': title_entry,
                'company': company_entry,
                'start_date': start_date_entry,
                'end_date': end_date_entry,
                'responsibilities': responsibilities_entry
            })

        add_button = tk.Button(self.work_experience_frame, text="Add Work Experience", command=add_work_experience)
        add_button.pack(pady=5)

    def create_education_widgets(self):
        self.education_frame = tk.LabelFrame(self.root, text="Education")
        self.education_frame.pack(pady=10, padx=10, fill=tk.X)

        self.education_entries = []

        def add_education():
            frame = tk.Frame(self.education_frame)
            frame.pack(pady=5, fill=tk.X)

            tk.Label(frame, text="Degree:").pack(side=tk.LEFT, padx=5)
            degree_entry = tk.Entry(frame, width=20)
            degree_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Institution:").pack(side=tk.LEFT, padx=5)
            institution_entry = tk.Entry(frame, width=20)
            institution_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Graduation Year:").pack(side=tk.LEFT, padx=5)
            graduation_year_entry = tk.Entry(frame, width=10)
            graduation_year_entry.pack(side=tk.LEFT, padx=5)

            self.education_entries.append({
                'frame': frame,
                'degree': degree_entry,
                'institution': institution_entry,
                'graduation_year': graduation_year_entry
            })

        add_button = tk.Button(self.education_frame, text="Add Education", command=add_education)
        add_button.pack(pady=5)

    def create_skills_widgets(self):
        tk.Label(self.root, text="Skills (comma separated):").pack(pady=5)
        self.skills_entry = tk.Entry(self.root, width=50)
        self.skills_entry.pack(pady=5)

    def create_achievements_widgets(self):
        tk.Label(self.root, text="Achievements (comma separated):").pack(pady=5)
        self.achievements_entry = tk.Entry(self.root, width=50)
        self.achievements_entry.pack(pady=5)

    def create_volunteer_work_widgets(self):
        tk.Label(self.root, text="Volunteer Work (comma separated):").pack(pady=5)
        self.volunteer_work_entry = tk.Entry(self.root, width=50)
        self.volunteer_work_entry.pack(pady=5)

    def create_references_widgets(self):
        self.references_frame = tk.LabelFrame(self.root, text="References")
        self.references_frame.pack(pady=10, padx=10, fill=tk.X)

        self.references_entries = []

        def add_reference():
            frame = tk.Frame(self.references_frame)
            frame.pack(pady=5, fill=tk.X)

            tk.Label(frame, text="Name:").pack(side=tk.LEFT, padx=5)
            name_entry = tk.Entry(frame, width=20)
            name_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Contact:").pack(side=tk.LEFT, padx=5)
            contact_entry = tk.Entry(frame, width=20)
            contact_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(frame, text="Relationship:").pack(side=tk.LEFT, padx=5)
            relationship_entry = tk.Entry(frame, width=20)
            relationship_entry.pack(side=tk.LEFT, padx=5)

            self.references_entries.append({
                'frame': frame,
                'name': name_entry,
                'contact': contact_entry,
                'relationship': relationship_entry
            })

        add_button = tk.Button(self.references_frame, text="Add Reference", command=add_reference)
        add_button.pack(pady=5)

    def submit(self):
        # Gather personal information
        personal_info = {
            'full_name': self.full_name_entry.get(),
            'email': self.email_entry.get(),
            'phone_number': self.phone_number_entry.get(),
            'location': self.location_entry.get(),
            'objective': self.objective_text.get("1.0", tk.END).strip(),
            'work_experience': [],
            'education': [],
            'skills': self.skills_entry.get().split(','),
            'achievements': self.achievements_entry.get().split(','),
            'volunteer_work': self.volunteer_work_entry.get().split(','),
            'references': []
        }

        # Gather work experience
        for entry in self.work_experience_entries:
            work_experience = {
                'job_title': entry['title'].get(),
                'company': entry['company'].get(),
                'start_date': entry['start_date'].get(),
                'end_date': entry['end_date'].get(),
                'responsibilities': entry['responsibilities'].get()
            }
            personal_info['work_experience'].append(work_experience)

        # Gather education
        for entry in self.education_entries:
            education = {
                'degree': entry['degree'].get(),
                'institution': entry['institution'].get(),
                'graduation_year': entry['graduation_year'].get()
            }
            personal_info['education'].append(education)

        # Gather references
        for entry in self.references_entries:
            reference = {
                'name': entry['name'].get(),
                'contact': entry['contact'].get(),
                'relationship': entry['relationship'].get()
            }
            personal_info['references'].append(reference)

        # Convert lists and dictionaries to JSON
        personal_info['work_experience'] = json.dumps(personal_info['work_experience'])
        personal_info['education'] = json.dumps(personal_info['education'])
        personal_info['references'] = json.dumps(personal_info['references'])

        # Save to database
        try:
            conn = psycopg2.connect(dbname="job_app_db", user="postgres", password="password", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_resume_info (full_name, email, phone_number, location, objective, work_experience, education, skills, achievements, volunteer_work, references)
                VALUES (%(full_name)s, %(email)s, %(phone_number)s, %(location)s, %(objective)s, %(work_experience)s, %(education)s, %(skills)s, %(achievements)s, %(volunteer_work)s, %(references)s)
            """, personal_info)
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Information saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Run the application
root = tk.Tk()
app = ResumeGUI(root)
root.mainloop()