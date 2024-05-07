# Object Detection and Measurement with YOLOv5, Camera Calibration, and Database Integration

This project combines object detection using YOLOv5 with camera calibration for measurement of detected objects. Additionally, it includes a user interface built with Tkinter for desktop application and a Node.js web API for displaying data stored in a database to the frontend using HTML, CSS, and JavaScript.

## Features

- Object detection using YOLOv5 with the COCO dataset
- Measurement functionality with camera calibration
- User interface built with Tkinter for desktop application
- Node.js web API for displaying data stored in a database
- Integration with a SQL database to store detected object results

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system
- Node.js installed on your system
- YOLOv5 and its dependencies installed
- Tkinter library installed (for desktop UI)
- Required Python packages installed (including `opencv`, `numpy`, `mssql`, etc.)
- SQL database server installed and configured

- Python Dependencies
  tkinter: For building the desktop user interface
  PIL: Python Imaging Library, used for image processing tasks
  opencv: OpenCV library for computer vision tasks
  numpy: Fundamental package for scientific computing with Python
  torch: PyTorch library for deep learning tasks
  pyodbc: Python library for interacting with ODBC databases

Node.js Dependencies
  express: Web framework for Node.js
  multer: Middleware for handling file uploads
  mssql: Microsoft SQL Server client for Node.js
  body-parser: Middleware for parsing incoming request bodies
  path: Node.js module for working with file paths
  fs: Node.js module for file system operations


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pratikdawkhar10/Object_detection_and_measurement_with_yolov5
    ```

2. Install Python dependencies:

    ```bash
    pip install tk pillow opencv-python numpy torch pyodbc
    ```

3. Install Node.js dependencies (if applicable):

    ```bash
    npm install express multer mssql path body-parser
    ```

## Usage

1. Run the object detection script:

    ```bash
    python obj_detection.py
    ```

2. Access the desktop application UI with detection as well as measurement:

    ```bash
    python UI_for_both_functionality.py
    ```

3. Start the Node.js web API (if applicable):

    ```bash
    node server.js
    ```

4. Access the web interface using a browser at `http://localhost:port` (replace `port` with the actual port number configured for the API).

## Database Configuration

- Ensure you have a SQL database server installed and running.
- Update the database configuration in the code with your database credentials.
- Create a table in your database to store detected object results.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
