import face_recognition
import numpy as np
from database import get_user_face_encoding

def process_frame(frame):
    """Processes the given frame and checks for face matches in the database."""
    face_encodings = face_recognition.face_encodings(frame)

    if len(face_encodings) == 0:
        return False, None

    user_id = 1  # Example: Fetching user 1 from database
    stored_encoding = get_user_face_encoding(user_id)

    if stored_encoding is not None:
        match = face_recognition.compare_faces([stored_encoding], face_encodings[0])[0]
        return match, user_id if match else None
    
    return False, None
