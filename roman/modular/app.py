import sys
import database as db
import auth
import personal_info
import job_offers

def main_menu():
    print("\n--- Job Application Assistant ---")
    print("1. Register")
    print("2. Login")
    print("3. Quit")
    return input("Choose an option: ")

def user_menu():
    print("\n--- User Menu ---")
    print("1. Manage Personal Information")
    print("2. Manage Job Offers")
    print("3. Generate Application Letter")
    print("4. Logout")
    return input("Choose an option: ")

def personal_info_menu():
    print("\n--- Personal Information ---")
    print("1. View Personal Information")
    print("2. Add/Update Personal Information")
    print("3. Back")
    return input("Choose an option: ")

def job_offer_menu():
    print("\n--- Job Offers ---")
    print("1. View Job Offers")
    print("2. Add/Update Job Offer")
    print("3. Delete Job Offer")
    print("4. Back")
    return input("Choose an option: ")

def main():
    conn = db.connect_to_db()
    if not conn:
        print("Failed to connect to the database. Exiting...")
        sys.exit(1)

    db.create_tables(conn)

    while True:
        choice = main_menu()
        if choice == "1":
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")

            user_id = auth.register_user(conn, username, email, password, first_name, last_name)
            if user_id:
                print("Registration successful! Please log in.")
            else:
                print("Registration failed.")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")

            user_id = auth.login_user(conn, username, password)
            if user_id:
                print("Login successful!")
                while True:
                    user_choice = user_menu()
                    if user_choice == "1":
                        while True:
                            pi_choice = personal_info_menu()
                            if pi_choice == "1":
                                info = personal_info.view_personal_info(conn, user_id)
                                if info:
                                    print(f"\nEmail: {info[0]}\nCV Path: {info[1]}\nSkills: {info[2]}")
                                else:
                                    print("No personal information found.")
                            elif pi_choice == "2":
                                email = input("Enter email: ")
                                cv_path = input("Enter CV path: ")
                                skills = input("Enter skills (comma-separated): ")
                                personal_info.add_or_update_personal_info(conn, user_id, email, cv_path, skills)
                                print("Personal information updated.")
                            elif pi_choice == "3":
                                break
                            else:
                                print("Invalid choice. Try again.")
                    elif user_choice == "2":
                        while True:
                            jo_choice = job_offer_menu()
                            if jo_choice == "1":
                                offers = job_offers.view_job_offers(conn, user_id)
                                if offers:
                                    for offer in offers:
                                        print(f"\nID: {offer[0]} - Title: {offer[1]}")
                                else:
                                    print("No job offers found.")
                            elif jo_choice == "2":
                                title = input("Enter job title: ")
                                company = input("Enter company name: ")
                                department = input("Enter department: ")
                                offer_url = input("Enter offer URL: ")
                                company_description = input("Enter company description: ")
                                offer_text = input("Enter offer text: ")
                                offer_id = input("Enter offer ID (leave empty for new): ")
                                if offer_id:
                                    offer_id = int(offer_id)
                                else:
                                    offer_id = None
                                job_offers.add_or_update_job_offer(conn, user_id, title, company, department, offer_url, company_description, offer_text, offer_id)
                                print("Job offer added/updated.")
                            elif jo_choice == "3":
                                offer_id = input("Enter the offer ID to delete: ")
                                job_offers.delete_job_offer(conn, offer_id, user_id)
                                print("Job offer deleted.")
                            elif jo_choice == "4":
                                break
                            else:
                                print("Invalid choice. Try again.")
                    elif user_choice == "3":
                        offers = job_offers.view_job_offers(conn, user_id)
                        if offers:
                            for offer in offers:
                                print(f"\nID: {offer[0]} - Title: {offer[1]}")
                            offer_id = input("Enter the offer ID to generate an application letter for: ")
                            offer_details = job_offers.view_job_offer_details(conn, offer_id, user_id)
                            if offer_details:
                                print(f"\nGenerating application letter for: {offer_details[0]} at {offer_details[1]}")
                                # Placeholder for OpenAI integration
                                print("Application letter generation feature coming soon...")
                            else:
                                print("Invalid offer ID.")
                        else:
                            print("No job offers found.")
                    elif user_choice == "4":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Try again.")
            else:
                print("Login failed.")
        elif choice == "3":
            print("Quitting the application.")
            break
        else:
            print("Invalid choice. Try again.")

    db.close_connection(conn)

if __name__ == "__main__":
    main()
