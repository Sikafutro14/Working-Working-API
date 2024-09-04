def add_or_update_personal_info(conn, user_id, email, cv_path, skills):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO personal_info (user_id, email, cv_path, skills)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET email = EXCLUDED.email,
                cv_path = EXCLUDED.cv_path,
                skills = EXCLUDED.skills
        """, (user_id, email, cv_path, skills))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error adding/updating personal info: {e}")

def view_personal_info(conn, user_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT email, cv_path, skills FROM personal_info WHERE user_id = %s
        """, (user_id,))
        info = cur.fetchone()
        cur.close()
        return info
    except Exception as e:
        print(f"Error viewing personal info: {e}")
        return None
