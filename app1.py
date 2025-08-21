import os
import uuid  # Used for generating unique filenames
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from aircraft_detection_module import detect_aircraft

# Initialize the Flask application
app = Flask(__name__)

# Define paths for uploading and processed images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(os.getcwd(), 'static', 'processed')

# Make sure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Main route to render the HTML template
@app.route('/')
def home():
    """Renders the main home page of the application."""
    return render_template('index.html')

# Route to serve processed images
@app.route('/static/processed/<filename>')
def processed_image(filename):
    """Serves a processed image from the processed folder."""
    return send_from_directory(PROCESSED_FOLDER, filename)

# Route to handle image uploads and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the image upload, processes it, and returns the result."""
    # Check if a file was uploaded
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file:
        # Generate a unique filename to avoid overwriting files
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = str(uuid.uuid4()) + file_extension
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)

        # Process the image with the detection module
        result = detect_aircraft(filepath)

        # Check the status from the dictionary returned by the module
        if result['status'] == 'success':
            # Everything worked, so create the URL and return the JSON
            processed_image_url = url_for('processed_image', filename=os.path.basename(result['processed_image_url']))
            
            return jsonify({
                'status': 'success',
                'processed_image_url': processed_image_url,
                'total_detections': result['total_detections']
            })
        else:
            # An error occurred, return the error message from the module
            return jsonify({'status': 'error', 'message': result['message']}), 500

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)