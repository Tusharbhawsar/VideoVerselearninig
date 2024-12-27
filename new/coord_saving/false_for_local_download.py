import urllib.request
from ultralytics import YOLO
import pandas as pd
import csv
import cv2
import os
import json

import torch
'''import utils'''

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
data = pd.read_csv("/home/multi-sy-23/Downloads/cricket_ballde/fasle/Cricketballcycle.csv")
img_urls = data["Source Url"].tolist()  # Ensure img_urls is a list of strings
tags = data["Tags"].tolist()  # Ensure tags is a list of strings

create_fold="/home/multi-sy-23/Downloads/cricket_ballde/fasle/dead/"
#Create folder to save images if it does not exist
# create_fold = "images"
# if not os.path.exists(create_fold):
#     os.makedirs(create_fold)

# Download images from URLs
# for url in img_urls:
#     try:
#         image_name = os.path.basename(urllib.parse.urlparse(url).path)
#         print(image_name)
#         download_path = os.path.join(create_fold, image_name)
#         urllib.request.urlretrieve(url, download_path)
#     except Exception as e:
#         print(f"Failed to download {url}: {e}")

# Load YOLO model
model = YOLO('/home/multi-sy-23/Downloads/cricket_ballde/fasle/yolov8n.pt')
#cls=[0]
# CSV file to save coordinates
new_csv = "new_coordinates.csv"

# Write header to CSV
with open(new_csv, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Type", "Original Id", "Tags", "Source Url", "annotation"])

# Process each downloaded image
for tag, url in zip(tags, img_urls):
    try:
        image_name = os.path.basename(urllib.parse.urlparse(url).path)
        image_path = os.path.join(create_fold, image_name)
        cap = cv2.imread(image_path)

        # Ensure cap is read correctly
        if cap is None:
            raise ValueError(f"Failed to read image from {image_path}")

        # Perform YOLO prediction
        #results = model.predict(cap,classes=cls,max_det=1)
        results = model.predict(cap,max_det=1)

        annotation = {"line": [], "point": [], "rect": [], "circle": [], "rectAndKeypoints": [], "polygon": []}

        for r in results:
            ty = "train"
            id_ = ""
            #tag="false"
            #url = "Source Url"
            boxes = r.boxes
            for box in boxes:
                coord = []
                b = box.xywh[0].tolist()  # get box coordinates in (x, y, width, height) format
                print(b)
                x = b[0]
                y = b[1]
                w = b[2]
                h = b[3]

                xmin = x - (w / 2)
                ymin = y - (h / 2)
                coord.extend([xmin, ymin, w, h])
                
                print(coord)
    
                c = box.cls  # class id
                #name = model.names[int(c)]  # class name
                name = "false"
                annotation["rect"].append(coord + [name])

        # Write to CSV
        with open(new_csv, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            #csvwriter.writerow([ty, id_, tag, url, json.dumps(annotation)])
            csvwriter.writerow([ty, id_, name, url, json.dumps(annotation)])

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
