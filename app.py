import os
import cv2
import numpy as np
import face_recognition
from flask import Flask, request, jsonify
from database import get_user_face_encoding
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Face Recognition API is Running!"})

@app.route("/scan", methods=["POST"])
def scan_face():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join("static", filename)
    file.save(filepath)

    # Load the uploaded image
    uploaded_image = face_recognition.load_image_file(filepath)
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)

    if len(uploaded_encoding) == 0:
        return jsonify({"error": "No face found in image"}), 400

    uploaded_encoding = uploaded_encoding[0]

    # Fetch stored face encodings from the database
    user_id, stored_encoding = get_user_face_encoding()
    if stored_encoding is None:
        return jsonify({"error": "No registered user found"}), 400

    # Compare faces
    match = face_recognition.compare_faces([stored_encoding], uploaded_encoding)[0]
    
    return jsonify({
        "user_id": user_id,
        "match": match
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
