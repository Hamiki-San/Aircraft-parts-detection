from ultralytics import YOLO

# 1. Load your .pt file
# Replace 'best.pt' with the actual path to your model file
# (e.g., 'yolov8n.pt', 'yolov8s.pt', or '/path/to/your/custom_model/best.pt')
model = YOLO('aircraft_engine.pt')

# 2. Access the 'names' attribute
# This attribute is a dictionary where keys are class IDs (indices)
# and values are the corresponding class names (strings).
class_names = model.names

# 3. Print the class names and their indices
print("Class Names and their Indices:")
for idx, name in class_names.items():
    print(f"Index: {idx}, Name: {name}")

# Example: If your model was trained on COCO dataset, you might see:
# Index: 0, Name: person
# Index: 1, Name: bicycle
# Index: 2, Name: car
# ... and so on for all 80 classes.

# If your model was custom-trained for 'aircraft-engine', you would likely see:
# Index: 0, Name: aircraft-engine