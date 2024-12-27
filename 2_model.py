import numpy as np
import json
import torch
import cv2,os
import sys
import glob
sys.path.append(os.path.abspath('../'))


ball_model = torch.hub.load('yolov5/', 'custom', path='weights/blur_ball.pt', source='local') 
basket_model = torch.hub.load('yolov5/', 'custom', path='weights/ball_basket.pt', source='local') 


def find_tracker_bb_sorted(file_type,folder_path,output):
    lst = []

    files = glob.glob(os.path.join(folder_path, f'*.{file_type}'))

    files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    for img_name in files:
        image = cv2.imread(img_name)
        results = ball_model(img_name) 
        res1 = results.pandas().xyxy[0]
        lst = []
        for idx in range(len(results.pandas().xyxy[0])):
            # if res1.iloc[idx].iloc[6] == 'person':
                if res1.iloc[idx].iloc[4] >= 0.10:
                    # print("image name and confidence",img_name.split('/')[-1],res1.iloc[idx].iloc[4])
                    xmin,ymin,xmax,ymax,confidence,name = res1.iloc[idx].iloc[0],res1.iloc[idx].iloc[1],res1.iloc[idx].iloc[2],res1.iloc[idx].iloc[3],res1.iloc[idx].iloc[4],res1.iloc[idx].iloc[5]    
                    cords = [int(xmin),int(ymin),int(xmax),int(ymax)]
                    lst.append(cords)
                    bb_img = cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    cv2.putText(image, str(res1.iloc[idx].iloc[4]), (int(xmin), int(ymin)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    
        results = basket_model(img_name) 
        res1 = results.pandas().xyxy[0]
        lst = []
        for idx in range(len(results.pandas().xyxy[0])):
            # if res1.iloc[idx].iloc[6] == 'person':
                if res1.iloc[idx].iloc[4] >= 0.10:
                    # print("image name and confidence",img_name.split('/')[-1],res1.iloc[idx].iloc[4])
                    xmin,ymin,xmax,ymax,confidence,name = res1.iloc[idx].iloc[0],res1.iloc[idx].iloc[1],res1.iloc[idx].iloc[2],res1.iloc[idx].iloc[3],res1.iloc[idx].iloc[4],res1.iloc[idx].iloc[5]    
                    cords = [int(xmin),int(ymin),int(xmax),int(ymax)]
                    lst.append(cords)
                    bb_img = cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    cv2.putText(image, str(res1.iloc[idx].iloc[4]), (int(xmin), int(ymin)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)     
                    
                    isWritten = cv2.imwrite(os.path.join(output,img_name.split('/')[-1]), bb_img)
        
        
# find_tracker_bb_sorted('jpg','/home/multi-sy-007/yolo/StrongSORT-YOLO/images1','/home/multi-sy-007/yolo/StrongSORT-YOLO/result1')
