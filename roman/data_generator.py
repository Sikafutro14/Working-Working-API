import random
import string
import faker
import psycopg2

def generate_random_password(length=8):
    """Generates a random password with letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email(first_name, last_name, domain="example.com"):
    """Generates a random email address."""
    return f"{first_name.lower()}.{last_name.lower()}@{domain}"

def generate_random_skills(faker, language):
    """Generates a random skills description based on the language."""
    skills = faker.job()
    return " ".join(skills.split()[:20])  # Limit to 20 words

def generate_random_offers(user_id, faker, language, num_offers=10):
    """Generates random offers for a user."""
    offers = []
    for _ in range(num_offers):
        company = faker.company()
        department = faker.job()
        offer_url = faker.url()
        company_description = faker.paragraph()
        offer_text = faker.paragraph()
        offers.append({
            "company": company,
            "department": department,
            "offer_url": offer_url,
            "company_description": company_description,
            "offer_text": offer_text,
            "status": random.randint(0, 2),  # 0: pending, 1: applied, 2: rejected
            "response": random.choice([True, False]),
            "user_id": user_id
        })
    return offers

def generate_random_data(faker):
    """Generates random data for the database tables."""
    users = [
        {"username": "juan_perez", "email": generate_random_email("Juan", "Perez", "example.es"), "password": generate_random_password()},
        {"username": "max_mustermann", "email": generate_random_email("Max", "Mustermann", "example.de"), "password": generate_random_password()},
        {"username": "john_doe", "email": generate_random_email("John", "Doe", "example.com"), "password": generate_random_password()}
    ]

    personal_info = [
        {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan_perez@example.es",
            "cv_path": "cv_juan_perez.pdf",
            "user_id": 1
        },
        {
            "first_name": "Max",
            "last_name": "Mustermann",
            "email": "max_mustermann@example.de",
            "cv_path": "cv_max_mustermann.pdf",
            "user_id": 2
        },
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john_doe@example.com",
            "cv_path": "cv_john_doe.pdf",
            "user_id": 3
        }
    ]

    skills = [
        {"skill": generate_random_skills(faker, "es"), "user_id": 1},
        {"skill": generate_random_skills(faker, "de"), "user_id": 2},
        {"skill": generate_random_skills(faker, "en"), "user_id": 3}
    ]

    offers = []
    offers.extend(generate_random_offers(1, faker, "es", 15))
    offers.extend(generate_random_offers(2, faker, "de", 12))
    offers.extend(generate_random_offers(3, faker, "en", 10))

    return users, personal_info, skills, offers

def insert_data(data, connection_string):
    """Inserts the given data into the database tables."""
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()

        # ... (insert data into tables as before)

        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    faker = faker.Faker()
    data = generate_random_data(faker)

    # Replace with your actual database connection details
    connection_string = "dbname=job_app_db user=postgres password=password host=localhost"

    insert_data(data, connection_string)