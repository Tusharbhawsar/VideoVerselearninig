import cv2
import json
import os
import glob


def draw_rect(json_file,imagepath,out_path):
    with open(json_file,"r") as file:
        data=json.load(file)
        # print(data)
        # data2=data
        counter=0

        for key,value in data.items():
            # imag_name=f"{key}.jpg"
            # print(imag_name)

            new=value[0]
            left=new["coordinates"][0]
            top=new["coordinates"][1]
            right=new["coordinates"][2]
            bottom=new["coordinates"][3]
            # start=(top,left)
            # end=(bottom,right)
            start = (left, top)
            end = (right, bottom)
            # print("coordinates:", start,end)
            counter+=1
            
            path_img=os.path.join(imagepath,f"{counter}.jpg")

            read_img=cv2.imread(path_img)
            # print(read_img)
            color = (255, 0, 0) 
            thickness = 2

            image = cv2.rectangle(read_img,start,end,color,thickness)
            save_path=os.path.join(out_path,f"{counter}.jpg")
            cv2.imwrite(save_path,image) 


json_path="/home/link-lap-24/Autoflip_verticle/miss_coord2.json"
img_path="/home/link-lap-24/Autoflip_verticle/frames_checked/"
save_out="/home/link-lap-24/Autoflip_verticle/out/"

draw_rect(json_path,img_path,save_out)

# import cv2
# import json
# import os
# import glob

# def draw_rect(json_file, imagepath, out_path):
#     with open(json_file, "r") as file:
#         data = json.load(file)
#         counter = 0

#         for key, value in data.items():
#             # print(key)
#             new = value[0]
#             left = new["coordinates"][0]
#             top = new["coordinates"][1]
#             right = new["coordinates"][2]
#             bottom = new["coordinates"][3]
#             # start = (left, top)
#             # end = (right, bottom)
#             start=(top,left)
#             end=(bottom,right)
#             counter += 1

#             # Construct the output file path
#             save_path = os.path.join(out_path, f"{counter}.jpg")

#             # Load the corresponding image file
#             img_filename = f"{key}.jpg"
#             img_file_path = os.path.join(imagepath, img_filename)
#             print(img_file_path)
#             read_img = cv2.imread(img_file_path)

#             # Draw rectangle on the image
#             color = (255, 0, 0) 
#             thickness = 2
#             image = cv2.rectangle(read_img, start, end, color, thickness)

#             # Save the modified image
#             cv2.imwrite(save_path, image)

# json_path = "/home/link-lap-24/Autoflip_verticle/miss_coord2.json"
# img_path = "/home/link-lap-24/Autoflip_verticle/frames_checked/"
# save_out = "/home/link-lap-24/Autoflip_verticle/out/"

# draw_rect(json_path, img_path, save_out)
