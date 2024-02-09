

class FacialRecognitionnHelper:
    
    ...
    
    def __init__(self):
        ...
        
    def match():
        # Process image
        image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
        matches = process_image(image)
        
    # Function to process image and return recognized faces
    def process_image(image):
        face_locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, face_locations)

        matches = []
        for face_encoding in encodings:
            for index, known_encoding in enumerate(encodings):
                distance = face_recognition.face_distance(face_encoding, known_encoding)
                if distance < 0.5:  # Adjust threshold based on your model and accuracy needs
                    matches.append({"id": student_ids[index], "name": student_names[index]})
                    break  # Only report the first match for each face

        return matches
    
    # Function to store encoding and information in the database
    def store_encoding_in_database(hashed_id, encoding, student_name):
        # Connect to database
        # Store hashed_id, encoding (encrypted), and student_name securely
        # ... (Database interaction logic goes here)
        # ...

from flask import Flask, request, jsonify, Response
import cv2
import face_recognition

# Load model and encoding data
model = "models/resnet50.h5"
encodings, student_ids, student_names = load_encodings_from_database()  # Replace with your loading logic

@app.route("/match", methods=["POST"])
def match_faces():
    # Authenticate/authorize request

    # Get image data or video stream
    image_data = request.files.get("image")
    video_stream = request.environ.get('werkzeug.io.BufferedReader')  # For video stream

    # Check for either image or video input
    if not image_data and not video_stream:
        return jsonify({"error": "Please provide either an image or a video stream."}), 400

    # Process image
    if image_data:
        image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
        matches = process_image(image)

    # Process video stream (more complex, requires frame capturing and processing)
    elif video_stream:
        matches = process_video(video_stream)
    else:
        return jsonify({"error": "Internal error."}), 500

    # Return recognized faces and IDs/names
    return jsonify({"matches": matches})
