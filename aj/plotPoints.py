# plotPoints.py

import cv2
import numpy as np
import os

img = np.ones((1080,1920,3),np.uint8)
labelsPath = "/home/multi-sy-008/Downloads/testModelv5/yolov5/runs/detect/exp7/labels"
allCords = []
for file in os.listdir(labelsPath):
    with open(os.path.join(labelsPath,file),"r") as pos:
        cords = pos.readlines()[0].split("\n")[0].split(" ")
        allCords.append(cords[1:])

index = 0
for point in allCords:
    cv2.circle(img,(int(point[0]),int(point[1])),2,(0,0,255),2)
    img = cv2.putText(img, str(index), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.7,  (0,255,0))

    index+=1

cv2.imshow("img",img)
cv2.imwrite(labelsPath.split("/")[-2]+".jpg",img,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
