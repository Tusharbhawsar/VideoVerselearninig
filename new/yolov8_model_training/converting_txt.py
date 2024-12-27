import pandas as pd
import json
import cv2
import glob


img_path="/home/multi-sy-23/yolov8_model_training/images/"
com_path= glob.glob(img_path + "*.jpeg")
# print(com_path)
# dddas="/home/multi-sy-23/yolov8_model_training/out/00c3e7c-033f-cc20-cce-fe320c0e0babjpg.jpeg"
# # im=cv2.imread(dddas)
# # h,w,_=im.shape
# # print(w)

df=pd.read_csv("/home/multi-sy-23/yolov8_model_training/cricket_pitch_detection.csv")
coor = df["annotation"]
url = df["SourceUrl"]

for i,j,m in zip (coor,url,com_path):
    file_name=m.split("/")[-1].split(".")[0]
    # print(file_name)
    data=json.loads(i)
    # print(j)
    xywh=data["rect"][0]

    x=xywh[0]
    y=xywh[1]
    w=xywh[2]
    h=xywh[3]
    # print(h)

    img = cv2.imread(m)
    img_height, img_width , _ = img.shape
    # print(img_height,img_width)
    

    # x_max = x + w  #complete width 
    # y_max = y + h  #complete heigh

    # #  Convert to YOLO format
    # x_center = (x + x_max) / 2 / img_width
    # y_center = (y + y_max) / 2 / img_height
    # width = (x_max - x) / w
    # height = (y_max - x) / h
    x_max = x + w / 2
    y_max = y + h / 2
    
    x_center = x_max / img_width
    y_center = y_max / img_height
    width = w / img_width
    height = h / img_height

    with open (f"{file_name}.txt" , "w") as a:
        a.write(f"0 {x_center} {y_center} {width} {height}\n")
    
    # with open(file_name, "w") as a:
    #     a.write(f"0 {x_center} {y_center} {width} {height}\n")

    print(x_center,y_center,width,height)