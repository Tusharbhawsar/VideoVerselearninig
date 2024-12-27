import pandas as pd
import json
import cv2
import glob
import shutil
import os
import random

img_path = "/home/multi-sy-23/yolov8_model_training/images"
label_path = "/home/multi-sy-23/yolov8_model_training/labels"

main_path = "dataset3"

train_img = os.path.join(main_path, "images/train")
val_img = os.path.join(main_path, "images/val")
train_lab = os.path.join(main_path, "labels/train")
val_lab = os.path.join(main_path, "labels/val")

os.makedirs(train_img, exist_ok=True)
os.makedirs(val_img, exist_ok=True)
os.makedirs(train_lab, exist_ok=True)
os.makedirs(val_lab, exist_ok=True)

images_files = []
for i in os.listdir(img_path):
    # print(len(i))
    if i.endswith(".jpeg") or i.endswith(".jpg") or i.endswith(".png"):
        images_files.append(i)
print(len(images_files  ))
random.shuffle(images_files)

spliting = int(0.8 * len(images_files))
train_split = images_files[:spliting]
val_split = images_files[spliting:]

for idx, img_file in enumerate(images_files):
    if idx < spliting:
        shutil.copy(os.path.join(img_path, img_file), train_img)
        shutil.copy(os.path.join(label_path, img_file.rsplit(".", 1)[0] + ".txt"), train_lab)
    else:
        shutil.copy(os.path.join(img_path, img_file), val_img)
        shutil.copy(os.path.join(label_path, img_file.rsplit(".", 1)[0] + ".txt"), val_lab)
