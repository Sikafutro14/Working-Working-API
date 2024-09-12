import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from user_auth import get_db_connection
from resume_generator import generate_resume_letter

class JobOfferHandler:
    def __init__(self, root, user_id):
        self.root = root
        self.current_user_id = user_id
        self.selected_offer_id = None
        self.setup_interface()

    def setup_interface(self):
        self.chat_log = ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_entry = tk.Entry(self.root, font=("Arial", 12))
        self.user_entry.pack(padx=10, pady=10, fill=tk.X)
        self.user_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 12))
        send_button.pack(pady=5)

        resume_button = tk.Button(self.root, text="Generate Resume", command=self.display_resume, font=("Arial", 12))
        resume_button.pack(pady=5)
        
        offer_button = tk.Button(self.root, text="Add Job Offer", command=self.show_offer_form, font=("Arial", 12))
        offer_button.pack(pady=5)

        select_offer_button = tk.Button(self.root, text="Select Job Offer", command=self.show_offer_selection, font=("Arial", 12))
        select_offer_button.pack(pady=5)

        update_info_button = tk.Button(self.root, text="Update Personal Info", command=self.show_update_info_form, font=("Arial", 12))
        update_info_button.pack(pady=5)

    def show_update_info_form(self):
        self.update_info_window = tk.Toplevel(self.root)
        self.update_info_window.title("Update Personal Information")

        # Fetch current personal info
        personal_info = self.fetch_personal_info()
        
        tk.Label(self.update_info_window, text="First Name:").pack(pady=5)
        self.first_name_entry = tk.Entry(self.update_info_window)
        self.first_name_entry.insert(0, personal_info.get('first_name', ''))
        self.first_name_entry.pack(pady=5)

        tk.Label(self.update_info_window, text="Last Name:").pack(pady=5)
        self.last_name_entry = tk.Entry(self.update_info_window)
        self.last_name_entry.insert(0, personal_info.get('last_name', ''))
        self.last_name_entry.pack(pady=5)

        tk.Label(self.update_info_window, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.update_info_window)
        self.email_entry.insert(0, personal_info.get('email', ''))
        self.email_entry.pack(pady=5)

        tk.Label(self.update_info_window, text="Background:").pack(pady=5)
        self.background_entry = tk.Text(self.update_info_window, height=5, width=40, wrap=tk.WORD)
        self.background_entry.insert(tk.END, personal_info.get('background', ''))
        self.background_entry.pack(pady=5)

        submit_button = tk.Button(self.update_info_window, text="Submit", command=self.update_personal_info)
        submit_button.pack(pady=20)

    def fetch_personal_info(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT first_name, last_name, email, background FROM personal_info WHERE user_id = %s", (self.current_user_id,))
                info = cursor.fetchone()
                return {
                    'first_name': info[0] if info else '',
                    'last_name': info[1] if info else '',
                    'email': info[2] if info else '',
                    'background': info[3] if info else ''
                }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch personal info: {e}")
            return {}

    def update_personal_info(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        background = self.background_entry.get("1.0", tk.END).strip()

        if not first_name or not last_name or not email:
            messagebox.showerror("Error", "First name, last name, and email are required!")
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO personal_info (user_id, first_name, last_name, email, background)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) 
                    DO UPDATE SET first_name = EXCLUDED.first_name,
                                  last_name = EXCLUDED.last_name,
                                  email = EXCLUDED.email,
                                  background = EXCLUDED.background
                """, (self.current_user_id, first_name, last_name, email, background))

                conn.commit()
                messagebox.showinfo("Success", "Personal information updated successfully!")
                self.update_info_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update personal info: {e}")

    def show_offer_form(self):
        self.offer_window = tk.Toplevel(self.root)
        self.offer_window.title("Add Job Offer")

        tk.Label(self.offer_window, text="Position:").pack(pady=5)
        self.position_entry = tk.Entry(self.offer_window)
        self.position_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Company:").pack(pady=5)
        self.company_entry = tk.Entry(self.offer_window)
        self.company_entry.pack(pady=5)

        tk.Label(self.offer_window, text="About Company:").pack(pady=5)
        self.about_entry = tk.Text(self.offer_window, height=5, width=40, wrap=tk.WORD)
        self.about_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Job Offer:").pack(pady=5)
        self.offer_entry = tk.Text(self.offer_window, height=5, width=40, wrap=tk.WORD)
        self.offer_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Application URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.offer_window)
        self.url_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Status (1 for active, 0 for inactive):").pack(pady=5)
        self.status_entry = tk.Entry(self.offer_window)
        self.status_entry.pack(pady=5)

        tk.Label(self.offer_window, text="Response Received (1 for Yes, 0 for No):").pack(pady=5)
        self.response_entry = tk.Entry(self.offer_window)
        self.response_entry.pack(pady=5)

        submit_button = tk.Button(self.offer_window, text="Submit", command=self.submit_job_offer)
        submit_button.pack(pady=20)

    def submit_job_offer(self):
        position = self.position_entry.get()
        company = self.company_entry.get()
        about = self.about_entry.get("1.0", tk.END).strip()
        offer = self.offer_entry.get("1.0", tk.END).strip()
        url = self.url_entry.get()
        status = self.status_entry.get()
        response = self.response_entry.get()

        if not position or not company or not about or not offer or not url or not status or not response:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO offers (user_id, position, company, about, offer, url, status, response)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.current_user_id, position, company, about, offer, url, status, response))

                conn.commit()
                messagebox.showinfo("Success", "Job offer added successfully!")
                self.offer_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit job offer: {e}")

    def fetch_job_offers(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, position, company
                    FROM offers
                    WHERE user_id = %s
                """, (self.current_user_id,))
                offers = cursor.fetchall()
                return offers
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch job offers: {e}")
            return []

    def show_offer_selection(self):
        self.offer_selection_window = tk.Toplevel(self.root)
        self.offer_selection_window.title("Select Job Offer")

        tk.Label(self.offer_selection_window, text="Select an offer to generate the resume for:", font=("Arial", 12)).pack(pady=10)

        job_offers = self.fetch_job_offers()

        self.offer_var = tk.StringVar(value="")
        for offer in job_offers:
            offer_id, position, company = offer
            offer_text = f"Position: {position}, Company: {company}"
            tk.Radiobutton(self.offer_selection_window, text=offer_text, variable=self.offer_var, value=str(offer_id)).pack(anchor="w")

        submit_button = tk.Button(self.offer_selection_window, text="Submit", command=self.save_selected_offer)
        submit_button.pack(pady=10)

    def save_selected_offer(self):
        selected_offer_id = self.offer_var.get()
        if not selected_offer_id:
            messagebox.showerror("Error", "Please select a job offer.")
            return

        self.selected_offer_id = selected_offer_id
        self.offer_selection_window.destroy()
        messagebox.showinfo("Success", "Job offer selected!")

    def display_resume(self):
        if not self.selected_offer_id:
            self.update_chat_log("No job offer selected. Please select an offer first.\n")
            return

        resume_text = generate_resume_letter(self.current_user_id, self.selected_offer_id)
        self.update_chat_log(f"RESUME LETTER:\n{resume_text}\n\n")

    def send_message(self, event=None):
        # Placeholder for send_message implementation
        pass

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message)
        self.chat_log.config(state=tk.DISABLED)
