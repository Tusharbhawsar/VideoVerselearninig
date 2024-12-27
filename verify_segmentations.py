import cv2, glob, os
import numpy as np

data_dir ="/home/link-lap-24/Downloads/himashu_data/project-1-at-2023-09-22-06-45-ef0f64b0" 
save_dir = "/home/link-lap-24/Downloads/segmentation_checking"


txt_dir = os.path.join(data_dir, 'labels')
image_dir = os.path.join(data_dir, 'images')
accepted_txt_dir = os.path.join(save_dir, 'accepted', 'labels')
accepted_image_dir = os.path.join(save_dir, 'accepted', 'images')
rejected_txt_dir = os.path.join(save_dir, 'rejected', 'labels')
rejected_image_dir = os.path.join(save_dir, 'rejected', 'images')
os.makedirs(accepted_txt_dir, exist_ok=True)
os.makedirs(accepted_image_dir, exist_ok=True)
os.makedirs(rejected_txt_dir, exist_ok=True)
os.makedirs(rejected_image_dir, exist_ok=True)

alpha = 0.5
label_files = []
count = 0
for i in glob.glob(txt_dir + "/*.txt"):
    label_files.append(i)
    count += 1

total_files = len(label_files)
for s in range(total_files):
    txt_path = label_files[s]
    file_name = txt_path.split("/")[-1].split(".")[0]

    with open(txt_path, 'r') as f:
        labels = f.read().splitlines()
    
    image_path = os.path.join(image_dir, f"{file_name}.jpg")
    img_format = ".jpg"
    if not os.path.exists(image_path):
        image_path = os.path.join(image_dir, f"{file_name}.png")
        img_format = ".png"
        if not os.path.exists(image_path):
            print(f"IMG NOT FOUND :: {image_path}")
            continue
    
    print(image_path, end=" :: ")
    img = cv2.imread(image_path)
    img_copy = img.copy()
    h,w = img.shape[:2]
    colors = [(0,0,255), (0,255,0)]
    for label in labels:
        class_id, *poly = label.split(' ')
        poly = np.asarray(poly,dtype=np.float16).reshape(-1,2) # Read poly, reshape
        poly *= [w,h] # Unscale
        color = colors[int(class_id)]
        # cv2.polylines(img, [poly.astype('int')], True, color, 2) # Draw Poly Lines
        cv2.fillPoly(img, [poly.astype('int')], color, cv2.LINE_AA) # Draw area
    img = cv2.addWeighted(img, alpha, img_copy, (1-alpha), 0)

    cv2.imshow('Segmentation Polygon', img)
    k = cv2.waitKey(0) & 0xff
    if k == ord('y'):
        cmd = f"mv {txt_path} {os.path.join(accepted_txt_dir, f'{file_name}.txt')}"
        os.system(cmd)
        cmd = f"mv {image_path} {os.path.join(accepted_image_dir, f'{file_name}{img_format}')}"
        os.system(cmd)
        print("accepted")
    elif k == ord('n'):
        cmd = f"mv {txt_path} {os.path.join(rejected_txt_dir, f'{file_name}.txt')}"
        os.system(cmd)
        cmd = f"mv {image_path} {os.path.join(rejected_image_dir, f'{file_name}{img_format}')}"
        os.system(cmd)
        print("rejected")
    elif k == 27: # press 'Esc' key to stop processing
        break
