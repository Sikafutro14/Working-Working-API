import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from faker import Faker

# Initialize Faker for fake data generation
fake = Faker()

# Fake list to store applied companies' details
applied_companies = []

def test():
    # Function to generate fake companies with job offers
    def generate_fake_companies():
        companies = []
        for _ in range(10):
            company_name = fake.company()
            departments = [fake.job() for _ in range(3)]
            offers = [{"department": dept, "url": fake.url()} for dept in departments]
            companies.append({"company_name": company_name, "offers": offers})
        return companies

    fake_companies = generate_fake_companies()

    # Fake user data
    user_info = {
        "Name": "John Doe",
        "Date of Birth": "1990-01-01",
        "Resume": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Country": "USA"
    }

    # Initialize Main App Window
    app2 = ctk.CTk()
    app2.title("Home Page")
    app2.geometry("800x600")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Set Color Scheme
    bg_color = "#01071a"
    fg_color = "#3053c7"
    app2.configure(bg=bg_color)

    # Create a Header Frame
    header_frame = ctk.CTkFrame(app2, fg_color=bg_color)
    header_frame.pack(fill="x", pady=10)

    # Create a content frame for dynamic content
    content_frame = ctk.CTkFrame(app2, fg_color=bg_color)
    content_frame.pack(fill="both", expand=True, pady=20)

    # Function to clear the content_frame
    def clear_content_frame():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # Function to display user info
    def show_user_info():
     clear_content_frame()  # Clear previous content

    # Creating the resume form within the content_frame (like in ResumeGUI)
    tk.Label(content_frame, text="Full Name:").pack(pady=5)
    full_name_entry = tk.Entry(content_frame)
    full_name_entry.pack(pady=5)

    tk.Label(content_frame, text="Email:").pack(pady=5)
    email_entry = tk.Entry(content_frame)
    email_entry.pack(pady=5)

    tk.Label(content_frame, text="Phone Number:").pack(pady=5)
    phone_number_entry = tk.Entry(content_frame)
    phone_number_entry.pack(pady=5)

    tk.Label(content_frame, text="Location:").pack(pady=5)
    location_entry = tk.Entry(content_frame)
    location_entry.pack(pady=5)

    tk.Label(content_frame, text="Objective:").pack(pady=5)
    objective_text = scrolledtext.ScrolledText(content_frame, height=5, width=40)
    objective_text.pack(pady=5)

    # Work Experience
    work_experience_frame = tk.LabelFrame(content_frame, text="Work Experience")
    work_experience_frame.pack(pady=10, padx=10, fill=tk.X)

    work_experience_entries = []

    def add_work_experience():
        frame = tk.Frame(work_experience_frame)
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

        work_experience_entries.append({
            'title': title_entry,
            'company': company_entry,
            'start_date': start_date_entry,
            'end_date': end_date_entry,
            'responsibilities': responsibilities_entry
        })

    tk.Button(work_experience_frame, text="Add Work Experience", command=add_work_experience).pack(pady=5)

    # Skills
    tk.Label(content_frame, text="Skills (comma separated):").pack(pady=5)
    skills_entry = tk.Entry(content_frame, width=50)
    skills_entry.pack(pady=5)

    # Achievements
    tk.Label(content_frame, text="Achievements (comma separated):").pack(pady=5)
    achievements_entry = tk.Entry(content_frame, width=50)
    achievements_entry.pack(pady=5)

    # Volunteer Work
    tk.Label(content_frame, text="Volunteer Work (comma separated):").pack(pady=5)
    volunteer_work_entry = tk.Entry(content_frame, width=50)
    volunteer_work_entry.pack(pady=5)

    # References
    references_frame = tk.LabelFrame(content_frame, text="References")
    references_frame.pack(pady=10, padx=10, fill=tk.X)

    references_entries = []

    def add_reference():
        frame = tk.Frame(references_frame)
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

        references_entries.append({
            'name': name_entry,
            'contact': contact_entry,
            'relationship': relationship_entry
        })

    tk.Button(references_frame, text="Add Reference", command=add_reference).pack(pady=5)

    # Submit button
    def submit_resume():
        # Collect and store all the information
        personal_info = {
            'full_name': full_name_entry.get(),
            'email': email_entry.get(),
            'phone_number': phone_number_entry.get(),
            'location': location_entry.get(),
            'objective': objective_text.get("1.0", tk.END).strip(),
            'skills': skills_entry.get().split(','),
            'achievements': achievements_entry.get().split(','),
            'volunteer_work': volunteer_work_entry.get().split(','),
            'references': []
        }

        # Process work experience
        personal_info['work_experience'] = [{
            'job_title': entry['title'].get(),
            'company': entry['company'].get(),
            'start_date': entry['start_date'].get(),
            'end_date': entry['end_date'].get(),
            'responsibilities': entry['responsibilities'].get()
        } for entry in work_experience_entries]

        # Process references
        personal_info['references'] = [{
            'name': entry['name'].get(),
            'contact': entry['contact'].get(),
            'relationship': entry['relationship'].get()
        } for entry in references_entries]

        # Here you can implement the database saving logic or further processing
        messagebox.showinfo("Success", "Resume Submitted")

    tk.Button(content_frame, text="Submit", command=submit_resume).pack(pady=20)

    # Function to create a resume
    def create_resume():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Enter Keywords for Resume:", fg_color=fg_color).pack(pady=10)
        keywords_entry = ctk.CTkEntry(content_frame)
        keywords_entry.pack(pady=10)

        def generate_resume():
            keywords = keywords_entry.get()
            if keywords:
                # Simulating ChatGPT-generated resume based on keywords
                resume = f"Generated resume using keywords: {keywords}\nExperience: ...\nSkills: ..."
                ctk.CTkLabel(content_frame, text=resume, fg_color=fg_color).pack(pady=10)
            else:
                messagebox.showwarning("Input Required", "Please enter some keywords.")

        ctk.CTkButton(content_frame, text="Generate Resume", command=generate_resume, fg_color=fg_color).pack(pady=10)

    # Function to ask ChatGPT
    def chat_with_gpt():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Ask ChatGPT anything:", fg_color=fg_color).pack(pady=10)
        question_entry = ctk.CTkEntry(content_frame, width=400)
        question_entry.pack(pady=10)

        chat_display = ctk.CTkTextbox(content_frame, width=500, height=200)
        chat_display.pack(pady=10)

        def ask_chatgpt():
            question = question_entry.get()
            if question:
                # Simulating ChatGPT response
                response = f"ChatGPT: The answer to '{question}' is ..."
                chat_display.insert(tk.END, f"You: {question}\n{response}\n\n")
            else:
                messagebox.showwarning("Input Required", "Please enter a question.")

        ctk.CTkButton(content_frame, text="Ask", command=ask_chatgpt, fg_color=fg_color).pack(pady=10)

    # Function to view job offers
    def view_job_offers():
        clear_content_frame()  # Clear previous content

        tree_frame = ctk.CTkFrame(content_frame)
        tree_frame.pack(pady=20)

        columns = ("Company", "Department", "Job URL")
        tree_view = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree_view.heading(col, text=col)
            tree_view.column(col, anchor="center")

        # Insert fake job data into the treeview
        for company in fake_companies:
            for offer in company['offers']:
                tree_view.insert('', tk.END, values=(company["company_name"], offer["department"], offer["url"]))

        tree_view.pack()

    # Function to apply for a job
    def applied_resume():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Enter Company Name:", fg_color=fg_color).pack(pady=10)
        company_entry = ctk.CTkEntry(content_frame)
        company_entry.pack(pady=10)

        ctk.CTkLabel(content_frame, text="Enter Job URL:", fg_color=fg_color).pack(pady=10)
        url_entry = ctk.CTkEntry(content_frame)
        url_entry.pack(pady=10)

        ctk.CTkLabel(content_frame, text="Enter Resume Details:", fg_color=fg_color).pack(pady=10)
        resume_entry = ctk.CTkEntry(content_frame)
        resume_entry.pack(pady=10)

        def apply_to_job():
            company = company_entry.get()
            url = url_entry.get()
            resume = resume_entry.get()

            if company and url and resume:
                applied_companies.append({"Company": company, "URL": url, "Resume": resume})
                messagebox.showinfo("Success", f"Successfully applied to {company}.")
            else:
                messagebox.showwarning("Input Required", "Please fill in all fields.")

        ctk.CTkButton(content_frame, text="Apply", command=apply_to_job, fg_color=fg_color).pack(pady=10)

    # Function to update applied companies
    def update_companies():
        clear_content_frame()  # Clear previous content

        if applied_companies:
            for company in applied_companies:
                company_info = f"Company: {company['Company']}, URL: {company['URL']}, Resume: {company['Resume']}"
                ctk.CTkLabel(content_frame, text=company_info, fg_color=fg_color).pack(pady=10)
        else:
            ctk.CTkLabel(content_frame, text="No applied companies yet.", fg_color=fg_color).pack(pady=10)

    # Add buttons to the header frame
    ctk.CTkButton(header_frame, text="Personal Info", command=show_user_info, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Create Resume", command=create_resume, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Ask ChatGPT", command=chat_with_gpt, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="View Job Offers", command=view_job_offers, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Applied Resume", command=applied_resume, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Update Applied Companies", command=update_companies, fg_color=fg_color).pack(side="left", padx=10)

    app2.mainloop()



