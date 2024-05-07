import torch
import cv2
import numpy as np
from pathlib import Path

# Load YOLOv5 model
model_path = Path("yolov5x6.pt")
model = torch.hub.load('ultralytics/yolov5:v6.0', 'custom', path=model_path)
model.eval()

# Load class names
classes = []
with open("coco2.names", "r") as f:
    classes = [line.strip() for line in f]

def object_detection(image_path):
    # Load image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    # Forward pass through the model
    with torch.no_grad():
        results = model(img_rgb)

    # Post-process the detections
    conf_threshold = 0.5

    # Accessing detections using 'xyxy' attribute
    for detection in results.xyxy[0]:
        scores = detection[4]
        class_id = int(detection[5])
        
        if scores > conf_threshold:
            x_min, y_min, x_max, y_max = detection[:4].tolist()

            # Draw bounding box
            color = (0, 255, 0)  # Green
            cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)

            # Print object name and confidence score
            object_name = classes[class_id]
            confidence_score = scores.item()
            print(f"Detected Object: {object_name}, Confidence Score: {confidence_score:.2f}")

    # Display the result
    cv2.imshow("Object Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image = ("images/person.jpg")
# Example usage
object_detection(image)
