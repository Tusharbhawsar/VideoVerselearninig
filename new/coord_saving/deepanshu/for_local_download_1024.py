import urllib.request
from ultralytics import YOLO
import pandas as pd
import csv
import cv2
import os
import numpy as np
import json

# Load image URLs and tags from the CSV file
data = pd.read_csv("/home/link-lap-24/jupyter_files/new/coord_saving/deepanshu/Rugby-03-09-2024-12-18-11.csv")
img_urls = data["Source Url"].tolist()  # Ensure img_urls is a list of strings
tags = data["Tags"].tolist()  # Ensure tags is a list of strings

# Define the folder path for saving images
create_fold = "/home/link-lap-24/jupyter_files/new/coord_saving/deepanshu/images/"
if not os.path.exists(create_fold):
    os.makedirs(create_fold)

# Download images from URLs
for url in img_urls:
    try:
        image_name = os.path.basename(urllib.parse.urlparse(url).path)
        download_path = os.path.join(create_fold, image_name)
        print(f"Downloading {image_name} to {download_path}")

        # Download and save the image
        urllib.request.urlretrieve(url, download_path)

        # Verify that the image was saved
        if os.path.exists(download_path):
            print(f"Successfully saved {image_name}")
        else:
            print(f"Failed to save {image_name}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Load YOLO model
model = YOLO('/home/link-lap-24/jupyter_files/new/coord_saving/deepanshu/WUS63Zj613PCC3y.pt')

# CSV file to save coordinates
new_csv = "new_coordinates.csv"

# Write header to CSV
with open(new_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Type", "Original Id", "Tags", "Source Url", "annotation"])

# Process each downloaded image
for tag, url in zip(tags, img_urls):
    try:
        # Define `ty` and `id_` at the beginning of each loop iteration
        ty = "train"  # Or any other relevant type
        id_ = ""  # Placeholder for Original Id, if not available

        image_name = os.path.basename(urllib.parse.urlparse(url).path)
        image_path = os.path.join(create_fold, image_name)
        cap = cv2.imread(image_path)

        # Ensure cap is read correctly
        if cap is None:
            raise ValueError(f"Failed to read image from {image_path}")

        # Perform YOLO prediction
        results = model.predict(cap, max_det=1, imgsz=1024)
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

                xmin = x - (w / 2)
                ymin = y - (h / 2)
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
