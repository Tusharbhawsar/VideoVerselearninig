import pandas as pd
import csv
import urllib
import cv2
import os
import numpy as np
import json
import torch
from ultralytics import YOLO

# Check if CUDA (GPU support) is available
if torch.cuda.is_available():
    # Configure PyTorch to use GPU
    device = torch.device("cuda")
    print("Using GPU for computation.")
else:
    # If CUDA is not available, use CPU
    device = torch.device("cpu")
    print("CUDA is not available. Using CPU for computation.")

# Load image URLs and tags from the CSV file
data = pd.read_csv("/home/multi-sy-23/Downloads/krishna/Hurling.csv")
img_urls = data["Source Url"].tolist()  # Ensure img_urls is a list of strings
tags = data["Tags"].tolist()  # Ensure tags is a list of strings

# Define the folder path for reading images
create_fold = "/home/multi-sy-23/Downloads/krishna/Frames"

# Load YOLO model
model = YOLO('/home/multi-sy-23/Downloads/krishna/6reS7XxIpyvxDQc.pt')

# CSV file to save coordinates
new_csv = "new_coordinates.csv"

# Write header to CSV
with open(new_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Type", "Original Id", "Tags", "Source Url", "annotation"])

# Process each downloaded image
for tag, url in zip(tags, img_urls):
    # Define `ty` and `id_` at the beginning of each loop iteration
    ty = "train"  # Or any other relevant type
    id_ = ""  # Placeholder for Original Id, if not available
    tag="player"
    # Define image_name and image_path before the try block
    image_name = os.path.basename(urllib.parse.urlparse(url).path)
    image_path = os.path.join(create_fold, image_name)
    
    try:
        # Read image from the existing folder
        cap = cv2.imread(image_path)

        # Ensure cap is read correctly
        if cap is None:
            raise ValueError(f"Failed to read image from {image_path}")

        # Perform YOLO prediction
        #results = model.predict(cap, max_det=1, classes=0,imgsz=1024)
        results = model.predict(cap, classes=0,imgsz=1024)
        results = results[0]
        result_box = results.obb.xywhr.cpu().numpy()
        labels = results.obb.cls.tolist()
        scores = np.array(results.obb.conf.tolist(), dtype="float").round(2)

        annotation = {"line": [], "point": [], "rect": [], "circle": [], "rectAndKeypoints": [], "polygon": []}

        for rect, label, score in zip(result_box.tolist(), labels, scores):
            try:
                print(rect, ">>>>>>>>") 
                coord = []

                x = rect[0]
                y = rect[1]
                w = rect[2]
                h = rect[3]
                rotation=rect[4]
                print(">>>>>>>>>>",rotation)
                if abs(rotation) > np.pi / 4:
                	w, h = h, w 
			
                xmin = x - (w / 2)
                ymin = y - (h / 2)
                #x2, y2 = x + w, y + h
                #coord.extend([xmin, ymin, w, h])
                coord.extend([xmin, ymin, w, h])

                # Ensure label is a valid integer index for model.names
                if isinstance(label, (int, float)):  # Check if label is a number
                    label = int(label)  # Ensure label is an integer
                    if 0 <= label < len(model.names):
                        name = model.names[label]  # class name
                        annotation["rect"].append(coord + [name])
                    else:
                        print(f"Invalid class ID: {label}")
                else:
                    print(f"Invalid label type: {type(label)}")

            except Exception as e:
                print(f"Error processing bounding box: {e}")

        # Write to CSV
        with open(new_csv, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([ty, id_, tag, url, json.dumps(annotation)])

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
