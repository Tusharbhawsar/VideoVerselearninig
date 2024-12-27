import glob
import cv2
import numpy as np
import urllib.request
import time
import json
import os


with open("runout.json") as r:
    df=json.load(r)
    while(True):

        try:
            for l,i in enumerate(df):
                urls=i["imageUrl"]
                import time

                # im_name=str(l)

                curr = time.time()
                print(l)
                img=urllib.request.urlopen(urls)
                print(img)
                arr = np.asarray(bytearray(img.read()), dtype="uint8")
    #             img = cv2.imdecode(arr, -1) # Load img as it is

                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

                data=i['annotations']['rect'][0:4]
                print(data)
                x1=data[0]
        #         print(x1)
                y1=data[1]

                x2=data[0] + data[2]
                y2=data[1] + data[3]

                image2=img[y1:y2, x1:x2]
                # cv2.imwrite(f"/home/multi-sy-003/cricket_celebration/crop/{curr}.png", image2)
                cv2.imwrite(f"""{curr}""".png", image2)

        #         print(x2)
        #         print(y2)
        except Exception as e:
            print(e)
