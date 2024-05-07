import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
#create deep neural network
import torch
from pathlib import Path
import pyodbc

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection and Measurement")

        # Option selection frame
        self.option_frame = tk.Frame(root)
        self.option_frame.pack()

        self.option_label = tk.Label(self.option_frame, text="Select an option:")
        self.option_label.grid(row=0, column=0, sticky="w")

        self.option_var = tk.StringVar()
        self.option_var.set("1")  # Default to Object Detection
        self.option_detect = tk.Radiobutton(self.option_frame, text="Object Detection", variable=self.option_var, value="1")
        self.option_detect.grid(row=0, column=1, sticky="w")

        self.option_measure = tk.Radiobutton(self.option_frame, text="Detect & Measurement", variable=self.option_var, value="2")
        self.option_measure.grid(row=1, column=1, sticky="w")

        # Distance input frame
        self.distance_frame = tk.Frame(root)
        self.distance_frame.pack()

        self.distance_label = tk.Label(self.distance_frame, text="Distance between object and camera (cm):")
        self.distance_label.grid(row=0, column=0, sticky="w")
        self.distance_entry = tk.Entry(self.distance_frame)
        self.distance_entry.grid(row=0, column=1, sticky="w")

        # Select image button
        self.select_btn = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_btn.pack()

        # Text box container to display data
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(fill="both", expand=True)

        self.text_box = tk.Text(self.text_frame, wrap="word", height=5, width=50)  # Adjust the height and width here
        self.text_box.pack(fill="both", expand=True)

        # Save to Database button
        self.save_btn = tk.Button(root, text="Save to Database", command=self.save_to_database)
        self.save_btn.pack()

        # Load YOLOv5 model
        self.model_path = Path("yolov5x6.pt")
        self.model = torch.hub.load('ultralytics/yolov5:v6.0', 'custom', path=self.model_path)
        self.model.eval()

        # Load class names
        self.classes = []
        with open("coco2.names", "r") as f:
            self.classes = [line.strip() for line in f]

        # SQL Server connection
        self.conn = pyodbc.connect(
            # add your SQL Server connection string here
        )

        # File path variable to store selected image path
        self.file_path = None

    def select_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.file_path:
            if self.option_var.get() == "1":
                self.perform_detection(self.file_path)  # Call perform_detection directly
            elif self.option_var.get() == "2":
                distance = float(self.distance_entry.get())
                self.obj_measurement(self.file_path, distance)

    def perform_detection(self, image_path):
        # Load image
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

        # Forward pass through the model
        with torch.no_grad():
            results = self.model(img_rgb)

        # Post-process the detections
        conf_threshold = 0.5

        # Accessing detections using 'xyxy' attribute
        detection_data = ""
        for detection in results.xyxy[0]:
            scores = detection[4]
            class_id = int(detection[5])
            
            if scores > conf_threshold:
                x_min, y_min, x_max, y_max = detection[:4].tolist()

                # Draw bounding box
                color = (0, 255, 0)  # Green
                cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)

                # Print object name and confidence score
                object_name = self.classes[class_id]
                confidence_score = scores.item()
                detection_data += f"Detected Object: {object_name}, Confidence Score: {confidence_score:.2f}\n"
                print(f"Detected Object: {object_name}, Confidence Score: {confidence_score:.2f}")

        # Resize the image for display
        scale_percent = 75  # You can adjust this percentage as needed
        new_width = int(img.shape[1] * scale_percent / 100)
        new_height = int(img.shape[0] * scale_percent / 100)
        resized_image = cv2.resize(img, (new_width, new_height))

        # Convert image back to RGB for PIL display
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(resized_image_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Create a new window to display the image
        panel = tk.Toplevel()
        panel.title("Object Detection Result")
        panel.geometry("800x600")

        panel.img_label = tk.Label(panel, image=img_tk)
        panel.img_label.image = img_tk
        panel.img_label.pack()

        self.text_box.delete(1.0, "end")
        self.text_box.insert("end", detection_data)

    def obj_measurement(self, image_path, dist):
        # Load image
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
            results = self.model(img_rgb)

        # Post-process the detections
        conf_threshold = 0.5

        # Accessing detections using 'xyxy' attribute
        measurement_data = ""
        for detection in results.xyxy[0]:
            scores = detection[4]
            class_id = int(detection[5])
            
            if scores > conf_threshold:
                x_min, y_min, x_max, y_max = detection[:4].tolist()

                # Calculate width and height
                w = x_max - x_min
                h = y_max - y_min

                # Calculate width and height in centimeters
                pixel_to_cm_ratio = fixed_distance_cm * focal_length_mm / (w * sensor_width_mm)
                object_width_cm = w * pixel_to_cm_ratio
                object_height_cm = h * pixel_to_cm_ratio

                # Draw bounding box
                color = (0, 255, 0)  # Green
                cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)

                # Print object name and measurements
                object_name = self.classes[class_id]
                print(f"Detected Object: {object_name}, Width: {object_width_cm:.2f} cm, Height: {object_height_cm:.2f} cm")
                # Print object name and measurements
                measurement_data += f"Detected Object: {self.classes[class_id]}, Width: {object_width_cm:.2f} cm, Height: {object_height_cm:.2f} cm\n"

        self.text_box.delete(1.0, "end")
        self.text_box.insert("end", measurement_data)
        
        # Resize image for display
        scale_percent = 50  # You can adjust this percentage as needed
        new_width = int(img.shape[1] * scale_percent / 100)
        new_height = int(img.shape[0] * scale_percent / 100)
        resized_image = cv2.resize(img, (new_width, new_height))

        # Display resized image
        self.display_image(resized_image)

    def save_to_database(self):
        image_path = self.file_path
        detected_objects = self.text_box.get(1.0, "end-1c")
        distance = self.distance_entry.get()

        # Split detected objects into individual object names
        detected_objects_list = [obj.split(":")[1].strip().split(',')[0] for obj in detected_objects.split("\n") if obj]

        # Prepare measurements
        measurement_data = ""
        if self.option_var.get() == "2":
            measurement_data = detected_objects  # Use detection data as measurements for option 2

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO DetectedObjects (ImagePath, DetectedObjects, fromDist, Measurements) VALUES (?, ?, ?, ?)",
                       (image_path, ', '.join(detected_objects_list), distance or None, measurement_data or None))
        messagebox.showinfo("Success", "Data saved to database successfully!")
        self.conn.commit()
        cursor.close()
        
    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        panel = tk.Toplevel()
        panel.title("Object Detection Result")
        panel.geometry("800x600")

        panel.img_label = tk.Label(panel, image=img)
        panel.img_label.image = img
        panel.img_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
