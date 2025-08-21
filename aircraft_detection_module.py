# aircraft_detection_module.py
import cv2
from ultralytics import YOLO
import os

# Load your trained YOLO model
try:
    model = YOLO('aircraft_engine.pt')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def detect_aircraft(image_path):
    """
    This function takes the path to an image file, runs aircraft detection on it,
    and returns the detection results.
    """
    if not model:
        return {"status": "error", "message": "Model could not be loaded."}

    try:
        frame = cv2.imread(image_path)
        if frame is None:
            return {"status": "error", "message": "Could not read the image file."}

        # IMPORTANT: Lowered the confidence threshold to 0.5 for better detection
        # This will make the model less strict about its detections.
        # You can adjust this value based on your model's performance.
        print("Running detection with a confidence threshold of 0.5...")
        results = model.predict(frame, conf=0.5, verbose=True) # verbose=True for debugging, confidence adjusment can be made here.
        result = results[0]

        print(f"Raw detections for {image_path}: {result.boxes.xyxy.tolist()}")
        
        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
            class_id = int(box.cls[0].item())
            prob = round(box.conf[0].item(), 2)
            detections.append({
                "class_id": class_id,
                "class_name": model.names[class_id],
                "bounding_box": [x1, y1, x2, y2],
                "confidence": prob
            })

        output_image = result.plot()
        output_dir = 'static/processed'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, output_image)
        
        processed_image_url = f"/{output_path.replace(os.path.sep, '/')}"

        # Check if any detections were made and update the total_detections accordingly
        total_detections = len(detections)
        if total_detections == 0:
            print("No detections found. Check your model and confidence threshold.")

        return {
            "status": "success",
            "total_detections": total_detections,
            "detections": detections,
            "processed_image_url": processed_image_url
        }

    except Exception as e:
        print(f"An error occurred during detection: {e}")
        return {"status": "error", "message": str(e)}
