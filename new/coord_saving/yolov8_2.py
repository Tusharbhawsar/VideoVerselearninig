import urllib.request
from ultralytics import YOLO
import pandas as pd
import urllib
import csv
import cv2
import os
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated


data=pd.read_csv("celebration_remain.csv")
img_urls=data["Source Url"]

create_fold="images"
if not os.path.exists(create_fold):
    os.makedirs(create_fold)

image_name=os.path.basename(img_urls)
download_path=os.path.join(create_fold,image_name)

for i in img_urls:
    urllib.request.urlretrieve(i,download_path)

model = YOLO('/home/link-lap-24/det_coordinate_saving/yBysLvx9bLUmo6w_v8.pt')

new_csv="new_coordinates.csv"

with open (new_csv , "w",newline="") as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(["Tag","annotation"])

bounding_box_list = []

for i in download_path:
    cap=cv2.imread(i)

while True:
    ret,frame=cap.read()
    results = model.predict(frame)


    for r in results:
        # annotator = Annotator(images)
        
        boxes = r.boxes
        for box in boxes:            
            b = box.xywh[0]  # get box coordinates in (left, top, right, bottom) format
            lis_cor=b.tolist()
            print(lis_cor)
            c = box.cls
            d = box.conf
            names=model.names[0]
            print(names)
            
            with open(new_csv,"a" ,newline="") as csvfile:
                csvwriter=csv.writer(csvfile)
                csvwriter.writerow([lis_cor,names])
