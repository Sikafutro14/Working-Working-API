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

        # Displaying Personal Info
        name_label = ctk.CTkLabel(content_frame, text=f"Name: {user_info['Name']}", fg_color=fg_color)
        name_label.pack(anchor="w", padx=10, pady=5)

        dob_label = ctk.CTkLabel(content_frame, text=f"Date of Birth: {user_info['Date of Birth']}", fg_color=fg_color)
        dob_label.pack(anchor="w", padx=10, pady=5)

        resume_label = ctk.CTkLabel(content_frame, text=f"Resume: {user_info['Resume']}", fg_color=fg_color)
        resume_label.pack(anchor="w", padx=10, pady=5)

        country_label = ctk.CTkLabel(content_frame, text=f"Country: {user_info['Country']}", fg_color=fg_color)
        country_label.pack(anchor="w", padx=10, pady=5)

        # Logout button
        logout_button = ctk.CTkButton(content_frame, text="Logout", command=app2.quit, fg_color="red")
        logout_button.pack(anchor="w", padx=10, pady=10)

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


