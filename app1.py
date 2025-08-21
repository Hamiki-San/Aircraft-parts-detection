# app.py
from flask import Flask, request, jsonify, render_template, url_for
import os
from aircraft_detection_module import detect_aircraft # <-- This is correct!

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No image selected for uploading"}), 400
    
    if file:
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        image_path = os.path.join(upload_folder, file.filename)
        file.save(image_path)
        
        # === Call your aircraft detection function ===
        detection_results = detect_aircraft(image_path)
        
        return jsonify(detection_results)

if __name__ == "__main__":
    app.run(debug=True)