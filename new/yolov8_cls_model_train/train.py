from ultralytics import YOLO

# model = YOLO('yolov8m-cls.pt')  # Replace 'n' with 's', 'm', etc. based on model size

# model.train(
#     data="/home/multi-sy-23/yolov8_cls_model_train/datasets",        # Path to dataset
#     epochs=80,              # Number of epochs
#     imgsz=1024,              # Image size
#     batch=8,               # Batch size
#     lr0=0.01,               # Initial learning rate
#     optimizer="Adam",        # Optimizer (SGD/Adam)
#     pretrained=True,        # Use pretrained weights
#     project="runs/train",   # Project directory
    
# )
# model.train(
#     data="/home/multi-sy-23/yolov8_cls_model_train/datasets",        
#     epochs=1,              # Number of epochs
#     imgsz=640,              # Image size
#     batch=8,               # Batch size
#     lr0=0.01,               # Initial learning rate
#     optimizer="Adam",        # Optimizer (SGD/Adam)
#     pretrained=True,        # Use pretrained weights
#     project="runs/train",   # Project directory
#     #name="yolov8_cls",      # Experiment name
# )

model = YOLO("/home/multi-sy-23/yolov8_cls_model_train/runs/train/train6/weights/best.pt")
# cls = [0]
results = model.predict(source="/home/multi-sy-23/yolov8_cls_model_train/transition",save=True,imgsz=1024)
print(results)
