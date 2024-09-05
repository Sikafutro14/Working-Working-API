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
            SELECT u.username, u.email, p.cv_path, p.skills 
            FROM users u
            JOIN personal_info p ON u.id = p.user_id
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
    username, email, cv_path, skills = personal_info

    # Create a prompt for the resume letter
    prompt = f"""
    Help me to create a resume letter, 
    My name is:{username}.
    Contact details: Email - {email}.
    Experience: {cv_path}.
    Skills: {skills}.
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