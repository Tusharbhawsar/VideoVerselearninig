from ultralytics import YOLO
import cv2
import os 
#import natsort

video_path = "/home/multi-sy-23/yolov8_model_training/1732620898_9440606.mp4"
player_model_path = "/home/multi-sy-23/yolov8_model_training/runs/detect/train9/weights/best.pt"
# ball_model_path = "/home/link-lap-24/Autoflip_verticle/auto_flip_test3/5uY7XAMfU35Gylj_golfball_v8.pt"

# model=YOLO(player_model_path)
# model=YOLO(ball_model_path)

# model.predict(source=video_path,save=True)

# Model2=YOLO("yolov8n.pt")

# person_cls=[0]

person=YOLO(player_model_path)

# Model2.predict(source=video_path, classes=person_cls,save=True,max_det=1,conf=0.30)
#person.predict(source=video_path,save=True,max_det=1,conf=0.30,imgsz=1080)
person.predict(source=video_path,save=True,imgsz=1080)
#for only last 50 frame detection
# fr_path="/home/link-lap-24/Autoflip_verticle/auto_flip_test3/1697963637_513412/"

# folder=natsort.natsorted(os.listdir(fr_path))
# Model2=YOLO("yolov8n.pt")

# length = len(folder)

# for i in range(length):
#     if i > length - 50:
#         imag_path=os.path.join(fr_path,folder[i])

#         person_cls=[0]

#         Model2.predict(source=imag_path, classes=person_cls,save=True,max_det=1,conf=0.90)
#         print(i)
