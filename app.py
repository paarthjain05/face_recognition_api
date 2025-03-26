import os
import face_recognition
import cv2
import numpy as np
import psycopg2
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DB_URL, sslmode="require")

def load_registered_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, image FROM users")
    users = {}

    for name, image_data in cur.fetchall():
        image = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)  

        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            users[name] = face_encodings[0]

    cur.close()
    conn.close()
    return users

registered_users = load_registered_users()

@app.route('/scan', methods=['GET'])
def scan_face():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        return jsonify({"error": "Webcam not accessible"})

    ret, frame = video_capture.read()
    video_capture.release()  

    if not ret:
        return jsonify({"error": "Failed to capture image from webcam"})

    rgb_frame = frame[:, :, ::-1]

    face_encodings = face_recognition.face_encodings(rgb_frame)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"})

    captured_face = face_encodings[0] 

    for user_name, user_encoding in registered_users.items():
        match = face_recognition.compare_faces([user_encoding], captured_face)[0]
        if match:
            return jsonify({"match": True, "user": user_name})

    return jsonify({"match": False, "user": "Unknown"})

if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5001))
    app.run(host=HOST, port=PORT, debug=True)
