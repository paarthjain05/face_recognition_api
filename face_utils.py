import face_recognition
import numpy as np

def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    
    if len(encodings) > 0:
        return np.array2string(encodings[0], separator=',')
    return None
