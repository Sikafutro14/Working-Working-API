import openai
from user_auth import get_db_connection

def fetch_personal_info(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.first_name, p.last_name, p.email, p.background
            FROM users u
            JOIN personal_info p ON u.id = p.user_id
            WHERE u.id = %s
        """, (user_id,))

        # Retrieve query results
        personal_info = cur.fetchone()

        cur.close()
        conn.close()

        return personal_info

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_offer_info(offer_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT position, company, about, offer, url
            FROM offers
            WHERE id = %s
        """, (offer_id,))

        offer_info = cur.fetchone()

        cur.close()
        conn.close()

        return offer_info

    except Exception as e:
        print(f"An error occurred while fetching offer info: {e}")
        return None

def generate_resume_letter(user_id, offer_id):
    personal_info = fetch_personal_info(user_id)
    offer_info = fetch_offer_info(offer_id)

    if not personal_info:
        return "User data not found."
    
    if not offer_info:
        return "Offer data not found."

    # Unpack the data
    first_name, last_name, email, background = personal_info
    position, company, about, offer, url = offer_info

    prompt = f"""
    Help me to create a resume letter.
    
    Personal Information:
    Name: {first_name} {last_name}
    Contact Email: {email}
    Background: {background}
    
    Job Offer Information:
    Position: {position}
    Company: {company}
    About Company: {about}
    Offer Details: {offer}
    Application URL: {url}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred while generating the resume: {e}")
        return "Error generating resume letter."