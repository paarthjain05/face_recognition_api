import os
import psycopg2
import face_recognition
import numpy as np
from flask import Flask, request, jsonify
from database import get_user_face_encoding
from face_recognition_service import process_frame

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_face():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    frame = face_recognition.load_image_file(file)

    match, user_id = process_frame(frame)
    return jsonify({"match": match, "user_id": user_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
