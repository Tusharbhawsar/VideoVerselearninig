#dashboard data fetch and convert data to yolo model
import requests
from PIL import Image
import shutil
import urllib
import os
import cv2
import json
import glob
import sys
import argparse
import random
import os.path

def rect_to_yolo_convert(json_path,dic):
    if not os.path.exists('data'):
        os.makedirs('data')
    images_save ="data/"
    f = open(json_path)
    store_values = []
    image_store = []
    count = 0
    for i in json.load(f):
        try:
            xmin,ymin,xmax,ymax,class_name,imageUrl, _id  = i['annotations']['rect'][0],i['annotations']['rect'][1],i['annotations']['rect'][2],i['annotations']['rect'][3],i['annotations']['rect'][4],i['imageUrl'],i['_id']
            count = count + 1
            name_id = imageUrl.split("/")[-1].split(".")[-2]
            img = Image.open(requests.get(imageUrl, stream = True).raw)
            path = images_save + name_id + '.jpg'
            if not os.path.exists(path):
                print(">>>>>>>>>>>>>>>>First time download>>>>>>>>>>>>>>>>>>>>>>")
                img.save(path)
            else:
                print(">>>>>>>>>>>>>>>>>>>>>already have this images process for multiclass calculation>>>>>>>>>>>>>>>>>>>")
            xmax,ymax = (xmax+xmin),(ymax+ymin)
            img = cv2.imread(images_save + name_id + '.jpg')
            h, w = img.shape[:2]
            xmin = xmin if xmin > 0 else 1
            ymin = ymin if ymin > 0 else 1
            xmax = xmax if xmax < w else w-1
            ymax = ymax if ymax < h else h-1
            box_w,box_h = xmax-xmin,ymax-ymin
            centre_x,centre_y= xmin+(box_w/2),ymin+(box_h/2)
            _x,_y,_w,_h = abs(centre_x/float(w)),abs(centre_y/float(h)), abs(box_w/float(w)),abs(box_h/float(h))
            data = str(dic[class_name]) + " " + str(_x) + " " + str(_y) + " " + str(_w) + " "+ str(_h)
            if _id in store_values:
                with open(images_save + name_id + '.txt', 'a') as f:
                    f.write("\n")
                    f.write(data)
            if _id not in store_values:
                with open(images_save + name_id + '.txt', 'w') as f:
                    f.write(data)
            store_values.append(_id)
            print(":::::::::::::::::::::Number_of_Images_Preprocess::::::::::::::::::::",count)
        except:
            print("Not Download ! invalid json or url of image")
            pass
    
    return images_save,str(count)

def spliting_train_test(PATH):
    outcome_split = "Done_Spliting"
    img_paths = glob.glob(PATH+'*.jpg')
    txt_paths = glob.glob(PATH+'*.txt')
    data_size = len(img_paths)
    r = 0.9
    train_size = int(data_size * 0.9)
    img_txt = list(zip(img_paths, txt_paths))
    random.seed(43)
    random.shuffle(img_txt)
    img_paths, txt_paths = zip(*img_txt)
    train_img_paths = img_paths[:train_size]
    train_txt_paths = txt_paths[:train_size]
    valid_img_paths = img_paths[train_size:]
    valid_txt_paths = txt_paths[train_size:]
    train_folder = PATH+'train/' 
    valid_folder = PATH+'test/'
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    if not os.path.exists(valid_folder):
        os.makedirs(valid_folder)
    def move(paths, folder):
        for p in paths:
            shutil.move(p, folder)
    move(train_img_paths, train_folder)
    move(train_txt_paths, train_folder)
    move(valid_img_paths, valid_folder)
    move(valid_txt_paths, valid_folder)
    return outcome_split,train_folder,valid_folder

def yolov_file_structure(mix_path,images_paths,labels_paths):
    
    outcome_final = "Done_Final_Step"
    
    images = sorted(glob.glob(mix_path + "*.jpg*"), key=lambda x : mix_path)

    labels = sorted(glob.glob(mix_path + "*.txt*"), key=lambda x : mix_path)

    for i in images:

        shutil.move(i,images_paths)

    for j in labels:
        
        shutil.move(j,labels_paths)    
    
    return outcome_final 

def value_arrange(inp):
    value = []
    for i in range(0,len(inp)):
        value.append(i)
    dic = {inp[i]: value[i] for i in range(len(value))}
    return dic    

def all_process_step(json_path,dic):

    images_save,count = rect_to_yolo_convert(json_path,dic)

    outcome_split,train_folder,valid_folder = spliting_train_test(images_save)

    if not os.path.exists(images_save + train_folder + 'images'):
        os.makedirs(images_save + train_folder + 'images')

    if not os.path.exists(images_save + train_folder + 'labels'):
        os.makedirs(images_save + train_folder + 'labels')    

    images_path_train = images_save + train_folder + 'images/'    
    labels_path_train = images_save + train_folder + 'labels/'

    if not os.path.exists(images_save + valid_folder + 'images'):
        os.makedirs(images_save + valid_folder + 'images')

    if not os.path.exists(images_save + valid_folder + 'labels'):
        os.makedirs(images_save + valid_folder + 'labels')    

    images_path_valid = images_save + valid_folder + 'images/'
    labels_path_valid = images_save + valid_folder + 'labels/'

    for_training_folder = yolov_file_structure(train_folder,images_path_train,labels_path_train)

    for_testing_folder = yolov_file_structure(valid_folder,images_path_valid,labels_path_valid)

    dic['Images'] = count

    with open("class_indexing" + '.txt', 'w') as f:
        f.write(str(dic))

        shutil.rmtree(train_folder)

        shutil.rmtree(valid_folder)

        print("::::::::::::::::::::::::::::::Done_All_Process:::::::::::::::::::::::::::::::::::::")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True)
args = vars(ap.parse_args())

json_path = args["input"]

inp = ['stable','ready','kick']   #only need to chance 

dic = value_arrange(inp)

all_process_step(json_path,dic)
