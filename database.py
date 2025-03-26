import os
import psycopg2
import numpy as np

DATABASE_URL = os.getenv("DATABASE_URL")

def get_user_face_encoding():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, face_encoding FROM users LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if row:
        user_id, encoding_str = row
        encoding_array = np.fromstring(encoding_str[1:-1], sep=',')
        return user_id, encoding_array
    return None, None
