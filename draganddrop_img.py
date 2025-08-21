import PySimpleGUI as sg
import cv2
import os
from ultralytics import YOLO # Import YOLO for loading the local model
import supervision as sv
import io
from PIL import Image

# --- Model Configuration ---
# Your local YOLOv8 trained model file
MODEL_FILE = 'best.pt'

# Check if the model file exists
if not os.path.exists(MODEL_FILE):
    sg.popup_error(f"Error: Model file '{MODEL_FILE}' not found. Please place it in the same directory as this script.")
    exit()

# Load the local YOLOv8 model once at the start
try:
    model = YOLO(MODEL_FILE)
    print("Local model loaded successfully.")
except Exception as e:
    sg.popup_error(f"Error loading local model: {e}")
    exit()

# --- Helper function to convert an OpenCV image to PySimpleGUI format ---
def convert_cv_to_bytes(frame):
    """
    Converts an OpenCV image (NumPy array) to a format
    that can be displayed by PySimpleGUI's sg.Image element.
    """
    # PySimpleGUI's Tkinter backend requires PNG or GIF
    # So we convert the frame to a PNG in-memory
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()
    return img_bytes

# --- Define the GUI Layout ---
# The layout is a list of lists, where each inner list is a row in the window
layout = [
    [sg.Text('Drag and Drop an image file here to detect airplanes!')],
    [sg.Input(key='-FILEPATH-', enable_events=True, visible=True)],
    [sg.Button('Process Image', key='-PROCESS-'), sg.Button('Exit', key='-EXIT-')],
    [sg.Image(key='-IMAGE-')],  # This element will display the annotated image
]

# Create the window
window = sg.Window('Airplane Detector', layout, resizable=True)

# --- Main Event Loop ---
while True:
    event, values = window.read()
    
    # Check if the user closed the window or clicked 'Exit'
    if event == sg.WINDOW_CLOSED or event == '-EXIT-':
        break

    # If a file path is entered (via drag and drop or browsing)
    if event == '-FILEPATH-':
        file_path = values['-FILEPATH-']
        if file_path and os.path.exists(file_path):
            print(f"File selected: {file_path}")
    
    # If the 'Process Image' button is clicked
    if event == '-PROCESS-':
        file_path = values['-FILEPATH-']
        
        # Check if a valid file path exists
        if not file_path or not os.path.exists(file_path):
            sg.popup_error("Please select a valid image file first.")
            continue
            
        try:
            # 1. Read the image using OpenCV
            frame = cv2.imread(file_path)
            if frame is None:
                sg.popup_error("Could not read the image file.")
                continue

            # 2. Perform local inference using the loaded model
            print("Performing local inference...")
            results = model(frame)

            # 3. Process results using Supervision
            detections = sv.Detections.from_ultralytics(results[0])
            
            # Get class names from the model (needed for labeling)
            class_names = model.names

            # Prepare labels for annotation
            labels = [
                f"{class_names[class_id]} {confidence:.2f}"
                for class_id, confidence
                in zip(detections.class_id, detections.confidence)
            ]

            # 4. Annotate the image with detections
            bounding_box_annotator = sv.BoundingBoxAnnotator()
            label_annotator = sv.LabelAnnotator()
            annotated_frame = bounding_box_annotator.annotate(scene=frame.copy(), detections=detections)
            annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
            
            # 5. Convert the annotated image to a format PySimpleGUI can use
            img_bytes = convert_cv_to_bytes(annotated_frame)

            # 6. Update the sg.Image element with the new image
            window['-IMAGE-'].update(data=img_bytes)

        except Exception as e:
            sg.popup_error(f"An error occurred: {e}")

# Close the GUI window
window.close()