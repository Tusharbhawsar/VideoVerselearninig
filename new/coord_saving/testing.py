import urllib.request
from ultralytics import YOLO
import pandas as pd
import urllib
import csv
import cv2
import os
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated

download_path="/home/link-lap-24/coord_saving/images/"
model = YOLO('/home/link-lap-24/coord_saving/Opan7ycDrDjQOQO.pt')

results = model.predict(download_path,save=True)

# for i in download_path:
#     cap=cv2.imread(i)

# while True:
#     ret,frame=cap.read()
#     results = model.predict(frame)


    # for r in results:
    #     # annotator = Annotator(images)
        
    #     boxes = r.boxes
    #     for box in boxes:            
    #         b = box.xywh[0]  # get box coordinates in (left, top, right, bottom) format
    #         lis_cor=b.tolist()
    #         print(lis_cor)
    #         c = box.cls
    #         d = box.conf
    #         names=model.names[0]
    #         print(names)
            