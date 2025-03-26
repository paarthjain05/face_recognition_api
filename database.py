import os
import psycopg2
import numpy as np

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_user_face_encoding(user_id):
    """Fetches the stored face encoding from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT face_encoding FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return np.array(eval(row[0]))  # Convert string to numpy array
    return None
