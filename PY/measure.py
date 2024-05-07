import torch
import cv2
from pathlib import Path
import numpy as np

# Load YOLOv5 model
model_path = Path("yolov5x6.pt")
model = torch.hub.load('ultralytics/yolov5:v6.0', 'custom', path=model_path)
model.eval()

# Load class names
classes = []
with open("coco2.names", "r") as f:
    classes = [line.strip() for line in f]

# Get layer names (not used in YOLOv5, but for compatibility)
layer_names = model.names

def obj_measurement(image , dist):
    # Load image
    image_path = image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    height, width, _ = img.shape

    # Fixed distance in centimeters
    fixed_distance_cm = dist  # Updated distance in centimeters

    # Realme 11 Pro camera specifications
    sensor_width_inches = 1.8  # Sensor size in inches
    focal_length_mm = 26.0  # Lens focal length in mm

    # Convert sensor size to mm
    sensor_width_mm = sensor_width_inches * 25.4

    # Calculate FOV(field of view)
    fov = 2 * np.arctan((sensor_width_mm / 2) / focal_length_mm)

    # Calculate focal length in pixels
    focal_length_pixels = width / (2 * np.tan(fov / 2))

    # Forward pass through the model
    with torch.no_grad():
        results = model(img_rgb)

    # Post-process the detections
    conf_threshold = 0.5
    nms_threshold = 0.4

    # Accessing detections using 'xyxy' attribute
    for detection in results.xyxy[0]:
        scores = detection[4]
        class_id = int(detection[5])
        
        if scores > conf_threshold:
            x_min, y_min, x_max, y_max = detection[:4].tolist()

            # Calculate width and height
            w = x_max - x_min
            h = y_max - y_min

            # Draw bounding box
            color = (0, 255, 0)  # Green
            cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)

            # Calculate width and height in centimeters
            pixel_to_cm_ratio = fixed_distance_cm * focal_length_mm / (w * sensor_width_mm)
            object_width_cm = w * pixel_to_cm_ratio
            object_height_cm = h * pixel_to_cm_ratio

            # Print object name and measurements
            print(f"Detected Object: {classes[class_id]}, Width: {object_width_cm:.2f} cm, Height: {object_height_cm:.2f} cm")

    # Resize image for display
    scale_percent = 50  # You can adjust this percentage as needed
    new_width = int(img.shape[1] * scale_percent / 100)
    new_height = int(img.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(img, (new_width, new_height))
    return resized_image

img = obj_measurement("images/bag.jpeg", 59)

# Display the result
cv2.imshow("Object Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
