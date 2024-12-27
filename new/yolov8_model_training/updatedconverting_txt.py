import pandas as pd
import json
import cv2
import wget
import os

img_path="images/"
txt_path="labels/"

if not os.path.exists(img_path):
	os.mkdir(img_path)
if not os.path.exists(txt_path):
	os.mkdir(txt_path)

df=pd.read_csv("Cricket-Ball-Detectio.csv")
coordinates = df["annotation"]
img_urls = df["Source Url"]

for coordinate, img_url, in zip(coordinates,img_urls):
    file_name=img_url.split("/")[-1].split(".")[0]
    data=json.loads(coordinate)
    xywh=data["rect"][0][:-1]

    x1=xywh[0]
    y1=xywh[1]
    w=xywh[2]
    h=xywh[3]

    img = wget.download(img_url,out=img_path)
    img = cv2.imread(img)
    img_height, img_width , _ = img.shape

    xcycwh = [x1+w/2, y1+h/2, w,h]
    xcycwh = [xcycwh[0]/img_width, xcycwh[1]/img_height, w/img_width, h/img_height]

    with open (f"{txt_path}/{file_name}.txt" , "w") as txt:
        txt.write(f"0 {xcycwh[0]} {xcycwh[1]} {xcycwh[2]} {xcycwh[3]}\n")
