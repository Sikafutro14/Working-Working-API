import psycopg2
import openai

def fetch_personal_info(user_id):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="job_app_db", 
            user="postgres", 
            password="password", 
            host="localhost", 
            port="5432"
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute("""
            SELECT first_name, last_name, email, cv_path, skills 
            FROM personal_info 
            WHERE id = %s
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
    first_name, last_name, email, cv_path, skills = personal_info

    # Create a prompt for the resume letter
    prompt = f"""
    Help me to create a resume letter, 
    My name is:{first_name}{last_name}.
    Contact details: Email - {email}.
    Experience: {cv_path}.
    Skills: {skills}.
    """

    # Get the response from ChatGPT
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=1000,
    )
    
    return response.choices[0].message.content