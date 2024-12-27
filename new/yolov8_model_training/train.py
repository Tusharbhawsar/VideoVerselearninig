from ultralytics import YOLO

model =YOLO("/home/multi-sy-23/yolov8_model_training/yolov8n.pt")

model.train(data="/home/multi-sy-23/yolov8_model_training/data.yaml",batch=8,epochs=30,imgsz=1024)
