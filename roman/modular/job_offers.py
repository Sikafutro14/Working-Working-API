def add_or_update_job_offer(conn, user_id, title, company, department, offer_url, company_description, offer_text, offer_id=None):
    try:
        cur = conn.cursor()
        if offer_id:
            cur.execute("""
                UPDATE offers
                SET title = %s,
                    company = %s,
                    department = %s,
                    offer_url = %s,
                    company_description = %s,
                    offer_text = %s
                WHERE id = %s AND user_id = %s
            """, (title, company, department, offer_url, company_description, offer_text, offer_id, user_id))
        else:
            cur.execute("""
                INSERT INTO offers (user_id, title, company, department, offer_url, company_description, offer_text)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, title, company, department, offer_url, company_description, offer_text))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error adding/updating job offer: {e}")

def view_job_offers(conn, user_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, title FROM offers WHERE user_id = %s", (user_id,))
        offers = cur.fetchall()
        cur.close()
        return offers
    except Exception as e:
        print(f"Error viewing job offers: {e}")
        return None

def view_job_offer_details(conn, offer_id, user_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT title, company, department, offer_url, company_description, offer_text
            FROM offers
            WHERE id = %s AND user_id = %s
        """, (offer_id, user_id))
        offer = cur.fetchone()
        cur.close()
        return offer
    except Exception as e:
        print(f"Error viewing job offer details: {e}")
        return None

def delete_job_offer(conn, offer_id, user_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM offers WHERE id = %s AND user_id = %s", (offer_id, user_id))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error deleting job offer: {e}")
