import glob
import json, cv2, os, shutil
import centroidtracker
import functools
import numpy as np
from scipy.ndimage import gaussian_filter1d


# video_url = "https://dwapv64icf8j2.cloudfront.net/3cxAmKXbu/1674964125.mp4"
video_url = "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173379.mp4"

data_folder = "./data/"
id_ = video_url.split("/")[-1].split(".")[0]
id_folder = data_folder + id_ + "/"
json_file = f"{id_}.json"
frame_path = f"data/{id_}/frames/"
cropped_folder = f"data/{id_}/cropped_frames/"
track_folder = id_folder + 'tracked_folder/'
moved_folder = id_folder + 'moved_folder/'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)

if not os.path.exists(id_folder):
    os.mkdir(id_folder)

if os.path.exists(cropped_folder):
    shutil.rmtree(cropped_folder)

if os.path.exists(frame_path):
    pass
else:
    os.mkdir(frame_path)
    os.system(f"ffmpeg -i {video_url} {frame_path}%d.jpg")

if os.path.exists(track_folder):
    shutil.rmtree(track_folder)
    if os.path.exists(moved_folder): shutil.rmtree(moved_folder)

os.mkdir(track_folder)
os.mkdir(cropped_folder)
os.mkdir(moved_folder)

data = json.load(open(json_file, "r"))
myKeys = list(map(int, data.keys()))
myKeys.sort()
data = {str(i): data[str(i)] for i in myKeys}


tracker = centroidtracker.CentroidTracker()
st_pt = 24
last_pts = []


def compare_from_old_pts(pts, compare_points, print_=True):
    # if type(pts) == tuple:
    #     pts = list(pts)
    #
    # if type(compare_points) == tuple:
    #     compare_points = list(compare_points)
    if print_: print(pts, compare_points)
    dist = np.linalg.norm(np.array(pts) - np.array(compare_points))
    # printing Euclidean distance
    if print_: print('Dist :: ', dist)
    if not print_: return dist
    return True if dist < 100 else False


ids = {}


for key, values in data.items():
    # print()
    if int(key) < st_pt:
        continue
    det = []
    points = []

    for value in values:
        xmin, ymin, xmax, ymax, conf, object_class = value["xmin"], value["ymin"], value["xmax"], \
            value["ymax"], value[
            "confidence"], value["name"]
        det.append([xmin,ymin,xmax,ymax])
        points.append([xmin, ymin])
        points.append([xmax, ymax])


    objects = tracker.update(det)
    # print(key)

    frame_key = f'{frame_path}{key}.jpg'
    out_key = f'{cropped_folder}{key}.jpg'

    if not os.path.exists(frame_key): continue
    img = cv2.imread(frame_key)
    # if len(objects) >= 1:
    #     img = cv2.imread(frame_key)
    # else:
    #     shutil.copy(frame_key, out_key)

    for (objectID, centroid) in objects.items():
        centroid = list(centroid)
        if objectID not in ids.keys():
            ids[objectID] = [{'cord': centroid, 'index': key}]
        else:
            ids[objectID].append({'cord': centroid, 'index': key})

        # print(objectID, centroid)
        x1, y1 = centroid
        rect = cv2.rectangle(img, (x1, y1), (x1 + 15, y1 + 10), (255, 0, 0), 2)
        rect = cv2.putText(rect, str(objectID), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2, cv2.LINE_AA, False)
        cv2.imwrite(f"{key}.jpg",rect)
    else:

    # if True:
    #     center_point = functools.reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
    #     x1, y1 = center_point
    #     x1, y1 = int(x1), int(y1)
        # crop = False
        #
        # if not last_pts:
        #     crop = True
        # else:
        #     crop = compare_from_old_pts(center_point, last_pts)

        # if crop:
        # rect = cv2.rectangle(img, (x1, y1), (x1 + 15, y1 + 10), (0, 255, 0), 2)
        # print(center_point, points)
        cv2.imwrite(out_key, rect)

        # if crop: last_pts = center_point


print(ids)








# import requests
# url_ball = "http://0.0.0.0:8016//v1/object-detection/yolov5s"

# # print(sorted(os.listdir(frame_path), key=lambda x: int(x.split("/")[-1].split(".")[0])))
# # exit()

# all_images = sorted(glob.glob(frame_path + '*.*'), key=lambda x: int(x.split("/")[-1].split(".")[0]))


# for file_name in all_images:
#     key = file_name.split("/")[-1].split(".")[0]
    
#     if int(key) < st_pt:
#         continue

#     # if int(key) > 80:
#     #     break
    
#     frame = cv2.imread(file_name)
#     _, img_encoded = cv2.imencode('.jpg', frame)

#     file = {'image': img_encoded.tobytes()}
#     openResponse = requests.post(url_ball, files=file)
#     det = []

#     print(f'Key :: {key}')
#     print(openResponse.json(), len(openResponse.json()))

#     if len(openResponse.json())>0:

#         # print(file_name,key)
#         for result in openResponse.json():
#             xmin,ymin,xmax,ymax,conf,object_class = result["xmin"],result["ymin"],result["xmax"],result["ymax"],result["confidence"], result["name"]
#             # balls.append([int(xmin),int(ymin)])
#             cv2.rectangle(frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,255),2)

#             det.append([xmin,ymin,xmax,ymax])
#             # points.append([xmin, ymin])
#             # points.append([xmax, ymax])
    
#     cv2.imwrite(f"{key}.jpg", frame)
#     objects = tracker.update(det)

#     # print(key)

#     frame_key = f'{frame_path}{key}.jpg'
#     out_key = f'{cropped_folder}{key}.jpg'

#     if not os.path.exists(frame_key): continue
#     img = cv2.imread(frame_key)
#     # if len(objects) >= 1:
#     #     img = cv2.imread(frame_key)
#     # else:
#     #     shutil.copy(frame_key, out_key)

#     for (objectID, centroid) in objects.items():
#         centroid = list(centroid)
#         if objectID not in ids.keys():
#             ids[objectID] = [{'cord': centroid, 'index': key}]
#         else:
#             ids[objectID].append({'cord': centroid, 'index': key})

#         # print(objectID, centroid)
#         x1, y1 = centroid
#         rect = cv2.rectangle(img, (x1, y1), (x1 + 15, y1 + 10), (255, 0, 0), 2)
#         rect = cv2.putText(rect, str(objectID), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                     (0, 0, 255), 2, cv2.LINE_AA, False)
#     # else:

#     # # if True:
#     # #     center_point = functools.reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
#     # #     x1, y1 = center_point
#     # #     x1, y1 = int(x1), int(y1)
#     #     # crop = False
#     #     #
#     #     # if not last_pts:
#     #     #     crop = True
#     #     # else:
#     #     #     crop = compare_from_old_pts(center_point, last_pts)

#     #     # if crop:
#     #     # rect = cv2.rectangle(img, (x1, y1), (x1 + 15, y1 + 10), (0, 255, 0), 2)
#     #     # print(center_point, points)
#     #     cv2.imwrite(out_key, rect)

#         # if crop: last_pts = center_point


# print('IDS', ids)


def find_id_total_movement(id_, cords):
    movement_list = []
    last_pt = cords[0]
    for index, cord in enumerate(cords[1:]):
        distance = compare_from_old_pts(last_pt, cord, print_=False)
        last_pt = cord
        movement_list.append(distance)

    print(f'Total average distance of id {id_} :: {sum(movement_list) / len(movement_list)}, Max movement {max(movement_list)} Min movement {min(movement_list)}')
    return sum(movement_list) / len(movement_list)


def delete_notMoving(coords):
    # print(coords)
    coords = coords.copy()

            # index = int(cord_i['index'])
    for i in range(len(coords)-1):
        if coords[i] is not None and coords[i+1] is not None:
            point1 = coords[i]['cord']
            point2 = coords[i+1]['cord']
            diff = [abs(point2[0] - point1[0]), abs(point2[1] - point1[1])]

            if diff[0] <5 and diff[1] <5:
                coords[i]['cord'] = [None,None]
    # print(coords)
    return coords


def remove_multi_trakcs(filtered_movement_list, upto):
    last_set = []
    cord_dict = {}

    for cords, id in filtered_movement_list:
        print(cords)
        cords = delete_notMoving(cords)
        for cord_i in cords:
            index = int(cord_i['index'])
            if index not in last_set:
                last_set.append(index)
                cord_dict[index] = cord_i['cord']
                cord_dict[index].append(id)
    
    # print("CORDS_DICT::",cord_dict)
    last_set = sorted(last_set)
    cindex = last_set[0]

    for index_items in range(cindex + 1, last_set[-1]):
        if index_items in last_set:
            cindex = index_items
            continue
        # cord_dict[index_items] = cord_dict[cindex]

        cord_dict[index_items] = [None,None]

        # cord_dict[index_items][-1] = 'filled'
    # print("CORDS_DICT::",cord_dict)

    start, end = last_set[0], last_set[-1]
    cords = {"x": [], "y": []}

    for items in range(start, end+1):
        x, y = cord_dict[items][0: 2]
        cords["x"].append(x)
        cords["y"].append(y)

    new_dict = {}



    import pandas as pd
    # x, y = [x[0] if x is not None else np.nan for x in actualBalls], [x[1] if x is not None else np.nan for x in actualBalls]
    x = list(cords['x'])
    y = list(cords['y'])

    x = pd.DataFrame(x)
    y = pd.DataFrame(y)


    x = x.interpolate("polynomial",order=2)
    y = y.interpolate("polynomial",order=2)

    x = np.array(x).tolist()

    y = np.array(y).tolist()

    # print(start,end,len(x))
    # x = list(gaussian_filter1d(cords['x'], 5))
    # y = list(gaussian_filter1d(cords['y'], 5))

    for index, items in enumerate(range(start, end)):
        if str(x[index][0]) != "nan":
            new_dict[items] = [x[index], y[index]]

    # print("***************************************************************\n")
    # print(new_dict)
    return new_dict



dist_thresh = 4
final_ids = {}
id_mapping = []
else_dist_mapping = []

for id, cord in ids.items():
    print("from ids",id, cord)
    average_distance = find_id_total_movement(id, [i['cord'] for i in cord])
    if average_distance > dist_thresh:
        final_ids[id] = cord
        id_mapping.append([id, average_distance])
    else:
        else_dist_mapping.append([id, average_distance])


# print('else_dist_mapping :: ', else_dist_mapping)
# print("final ids",final_ids)
all_frames = glob.glob(frame_path + '*.jpg')
if final_ids:
    mapped_distance = sorted(id_mapping, key=lambda x: x[-1])[:: -1]
    all_ids = [[final_ids[i[0]], i[0]] for i in mapped_distance]
    cords_dict = remove_multi_trakcs(all_ids, len(all_frames))

    # print("cords_dict::",cords_dict.items())
    img_cord = np.ones((1080,1920,3),np.uint8)
    doneCords = []
    for image_key, img_cords in cords_dict.items():
        full_key = track_folder + str(image_key) + '.jpg'
        frame_key = frame_path + str(image_key) + '.jpg'
        print(img_cords,image_key)
        x1, y1 = img_cords
        img = cv2.imread(frame_key)
        # print(x1,y1,img_cords,image_key)
        try:x1= int(x1[0]) 
        except: int(x1)
        try:y1 = int(y1[0])
        except: y1 = int(y1)
        rect = cv2.rectangle(img, (x1, y1), (x1 + 15, y1 + 10), (255, 0, 0), 2)
        cv2.circle(img,(x1,y1),3,(255,0,0),3)

        # rect = cv2.putText(rect, str(track_id), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (0, 0, 255), 2, cv2.LINE_AA, False)
        cv2.imwrite(full_key, rect)
        cv2.circle(img_cord,(x1,y1),3,(255,0,0),3)
        cv2.imshow("FRAME",img)
        cv2.waitKey(1)
        doneCords.append([x1,y1])

    cv2.imwrite("1675173025.jpg",img_cord)
    print("Done cords",doneCords)

for index, i in enumerate(sorted(glob.glob(track_folder + '*.jpg'), key=lambda x: int(x.split("/")[-1].split(".")[0])), 1):
    shutil.copy(i, moved_folder + str(index) + '.jpg')


