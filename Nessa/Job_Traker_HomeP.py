import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from faker import Faker

# Initialize Faker for fake data generation
fake = Faker()

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
    content_frame = ctk.CTkFrame(app2, fg_color="#01071a", bg_color=bg_color)
    content_frame.pack(fill="both", expand=True, pady=20)


    # Function to clear the content_frame
    def clear_content_frame():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # Function to display user info
    def show_user_info():
        clear_content_frame()  # Clear previous content
        # Dummy User Info
        user_info = {
            "Username": "john_doe",
            "Resume": "resume_link.pdf",
            "CV": "cv_link.pdf"
        }
        for i, (key, value) in enumerate(user_info.items()):
            ctk.CTkLabel(content_frame, text=f"{key}: {value}", fg_color=fg_color).pack(pady=10)

    # Function to create a resume by calling an API
    def create_resume():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Enter Keywords for Resume:", fg_color=fg_color).pack(pady=10)
        keywords_entry = ctk.CTkEntry(content_frame)
        keywords_entry.pack(pady=10)

        def generate_resume():
            keywords = keywords_entry.get()
            if keywords:
                # Simulating API Call to Generate Resume with Keywords
                resume = f"Generated resume with the following keywords: {keywords}"
                messagebox.showinfo("Resume Generated", resume)
            else:
                messagebox.showwarning("Input Required", "Please enter some keywords.")
        
        ctk.CTkButton(content_frame, text="Generate Resume", command=generate_resume, fg_color=fg_color).pack(pady=10)

    # Function to communicate with ChatGPT
    def chat_with_gpt():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Ask ChatGPT anything:", fg_color=fg_color).pack(pady=10)

        question_entry = ctk.CTkEntry(content_frame, width=400)
        question_entry.pack(pady=10)

        def ask_chatgpt():
            question = question_entry.get()
            if question:
                # Simulating API call to ChatGPT
                response = f"ChatGPT response for '{question}'"
                messagebox.showinfo("ChatGPT Response", response)
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

    # Function to update applied companies
    def update_companies():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Enter company name to update application status:", fg_color=fg_color).pack(pady=10)
        company_name_entry = ctk.CTkEntry(content_frame)
        company_name_entry.pack(pady=10)

        def update_status():
            company_name = company_name_entry.get()
            if company_name:
                messagebox.showinfo("Updated", f"Updated application status for {company_name}")
            else:
                messagebox.showwarning("Input Required", "Please enter a company name.")

        ctk.CTkButton(content_frame, text="Update", command=update_status, fg_color=self.dark_blue).pack(pady=10)

    # Function to delete old records
    def delete_records():
        clear_content_frame()  # Clear previous content

        ctk.CTkLabel(content_frame, text="Enter company name to delete record:", fg_color=fg_color).pack(pady=10)
        company_name_entry = ctk.CTkEntry(content_frame)
        company_name_entry.pack(pady=10)

        def delete_record():
            company_name = company_name_entry.get()
            if company_name:
                messagebox.showinfo("Deleted", f"Deleted application for {company_name}")
            else:
                messagebox.showwarning("Input Required", "Please enter a company name.")

        ctk.CTkButton(content_frame, text="Delete", command=delete_record, fg_color=fg_color).pack(pady=10)

    # Adding Buttons to Header Frame (Aligned Left to Right)
    ctk.CTkButton(header_frame, text="Personal Info", command=show_user_info, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Create Resume", command=create_resume, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Ask ChatGPT", command=chat_with_gpt, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="View Job Offers", command=view_job_offers, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Update Applied Companies", command=update_companies, fg_color=fg_color).pack(side="left", padx=10)
    ctk.CTkButton(header_frame, text="Delete Records", command=delete_records, fg_color=fg_color).pack(side="left", padx=10)

    app2.mainloop()
