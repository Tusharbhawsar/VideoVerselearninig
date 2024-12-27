# import cv2
# import numpy as np
# from ultralytics import YOLO

# video = cv2.VideoCapture("/home/link-lap-24/Autoflip_verticle/out23.mp4")
# model = YOLO("/home/link-lap-24/Autoflip_verticle/5uY7XAMfU35Gylj_golfball_v8.pt")

# out = cv2.VideoWriter("30fps2.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (606, 1080))
# counter = 0

# while video.isOpened():
#     ret, frame = video.read()
#     if not ret:
#         break
    
#     result = model.predict(frame)
#     for r in result:
#         boxes = r.boxes
#         for box in boxes:
#             b = box.xyxy[0]
#             new = b.tolist()
#             print(new)
#             x1 = new[0]
#             x2 = new[2]
#             y1 = new[1]
#             y2 = new[3]
#             row = int((y1 + y2) / 2)
#             column = int((x1 + x2) / 2)
#             print("after divide values:", column)
#             top = 0
#             bottom = 1080
#             left = column - 303
#             right = left + 606
#             print("start cropping point:", left)
            
           
#     cropped_frm = frame[top:bottom, left:right]
#     out.write(cropped_frm)
    
# video.release()
# out.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np
# from ultralytics import YOLO

# video = cv2.VideoCapture("/home/link-lap-24/Autoflip_verticle/out23.mp4")
# model = YOLO("/home/link-lap-24/Autoflip_verticle/5uY7XAMfU35Gylj_golfball_v8.pt")

# out = cv2.VideoWriter("expp.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (606, 1080))
# counter = 0

# while video.isOpened():
#     ret, frame = video.read()
#     if not ret:
#         break
    
#     result = model.predict(frame)
#     print(result)
    

#     cropped_frm = frame[0:1080, 0:606]
#     out.write(cropped_frm)

#     if len(result)==0:
#         out.write(frame)
#     else:
#         for r in result:
#             boxes = r.boxes
#             for box in boxes:
#                 b = box.xyxy[0]
#                 new = b.tolist()
#                 print(new)
#                 x1 = new[0]
#                 x2 = new[2]
#                 y1 = new[1]
#                 y2 = new[3]
#                 row = int((y1 + y2) / 2)
#                 column = int((x1 + x2) / 2)
#                 print("after divide values:", column)

#                 top = 0
#                 bottom = 1080
#                 left = abs(column - 303)
#                 right = left + 606
#                 print("start cropping point:", left)
#                 cropped_frm = frame[top:bottom, left:right]
#                 out.write(cropped_frm)
    # if len(result) == 0:  # If no detections, write the original frame to output
    #     out.write(frame)

# video.release()
# out.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
from ultralytics import YOLO
import json

video = cv2.VideoCapture("/home/link-lap-24/Autoflip_verticle/golf1.mp4")
model = YOLO("/home/link-lap-24/Autoflip_verticle/5uY7XAMfU35Gylj_golfball_v8.pt")

out = cv2.VideoWriter("golf1_out.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (606, 1080))
counter = 0
coord={}


while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    counter+=1 
    
    result = model.predict(frame)
    crop_final = []
    miss_cor = []
    for r in result:
        boxes = r.boxes
        key=r.keypoints
        print("keys_info:",key)
        for box in boxes:
            # print(box)
            b = box.xyxy[0]
            new = b.tolist()
            # print(new)
            clas_name=box.cls
            print(clas_name)
            trk_not=box.is_track
            print("class_info:",clas_name)
            # print(trk_not)
            x1 = new[0]
            x2 = new[2]
            y1 = new[1]
            y2 = new[3]
            row = int((y1 + y2) / 2)
            column = int((x1 + x2) / 2)

            top = 0
            bottom = 1080
            left = abs(column - 303)
            right = left + 606
            
            crop_final.append([top,bottom,left,right])

    top2 = 0
    bottom2 = 1080
    left2 = 0
    right2 = 606

    miss_cor.append([top2,bottom2,left2,right2])
    print("crop final:", miss_cor)

    if not crop_final:
        coord[f"img_{counter}.jpg"]=miss_cor
        print("not deteced coord saved")
    else:
        coord[f"img_{counter}.jpg"]=crop_final 
        print("deteced coord saved")   


    
    for key,value in coord.items():
        print(key)     
        final_top=value[0][0]
        print("start point >>>>>>>>>>>>>>>>")
        final_bottom=value[0][1]
        final_left=value[0][2]
        final_right=value[0][3]

    cropped_frm = frame[final_top:final_bottom, final_left:final_right]
    out.write(cropped_frm)


video.release()
out.release()
cv2.destroyAllWindows()

with open("tracking_test.json","w") as file:
    json.dump(coord,file)