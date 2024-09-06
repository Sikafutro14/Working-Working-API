import psycopg2
import openai
from user_auth import get_db_connection

def fetch_personal_info(user_id):
    try:
        conn = get_db_connection()

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute("""
            SELECT p.full_name, p.email, p.phone_number, p.location, p.objective 
            FROM users u
            JOIN details p ON u.id = p.user_id
            WHERE u.id = %s
        """, (user_id,))

        # Retrieve query results
        personal_info = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return personal_info

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_resume_letter(user_id):
    personal_info = fetch_personal_info(user_id)

    if not personal_info:
        return "User data not found."

    # Unpack the data
    full_name, email, phone_number, location, objective = personal_info

    # Create a prompt for the resume letter
    prompt = f"""
    Help me to create a resume letter, 
    My name is:{full_name}.
    Contact details: Email - {email}.
    Phone Number: {phone_number}.
    Location: {location}.
    Objective: {objective}.
    """

    # Get the response from ChatGPT
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