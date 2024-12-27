import numpy as np
import requests, cv2, io, glob, os, uuid, shutil, json
from scenedetect import detect, ContentDetector
import centroidtracker


# https://d1zxk9teuo4ijt.cloudfront.net/b9wZTWg9e/1675921478.mp4
# https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173153.mp4
# https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200074.mp4
# https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200492.mp4
# https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173611.mp4
# https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675172752.mp4
# https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173069.mp4
# https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200260.mp4
# https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173611.mp4


tracker = centroidtracker.CentroidTracker()
video_url = "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035255.mp4"
api_path = "http://localhost:8016/v1/object-detection/yolov5s2"
data_path = "./data/"
uid = 'test_1' #str(uuid.uuid4())
folder_path = data_path + uid + '/'
frames_path = folder_path + 'frames/'
crop_folder = folder_path + 'crop/'
if os.path.exists(folder_path): shutil.rmtree(folder_path)
os.mkdir(folder_path)
os.mkdir(frames_path)
os.mkdir(crop_folder)


if not os.path.exists(data_path): os.mkdir(data_path)


# def extract_frame(video_url, start_time, end_time, folder_path):
#     end_time = end_time - start_time
#     cmd = f"ffmpeg -ss {start_time} -i {video_url} -t {end_time} -qscale:v 0 {folder_path}%d.jpg"
#     print(f'Cmd to execute :: {cmd}')
#     os.system(cmd)
#     return sorted(glob.glob(folder_path + "*.*"), key=lambda x: int(x.split("/")[-1].split(".")[0]))




def extract_frame(video_url, start_time, end_time, folder_path):
    # print(files)
    # self.fileName = self.videoUrl.split("/")[-1]
    print("exists") if os.path.exists(folder_path) else os.mkdir(folder_path)
    # # os.system(f" cd {folder}")
    # os.system(f"ffmpeg -i {videoUrl} -s {c_w}x{c_h} -vf 'fps={str(fps)}' '{folder}/%04d.jpg' ")
    # os.system(f"ffmpeg -i {videoUrl}  '{folder}/%04d.jpg' ")
    print(start_time,end_time)
    vs = cv2.VideoCapture(video_url)
    frameNu = 0
    while vs.isOpened():
        ret, frame = vs.read()
        if not ret:
            break
        if start_time*50<frameNu<end_time*50:
            cv2.imwrite(
            f"{folder_path}/{frameNu}.jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), 100],
            )
        frameNu += 1
    vs.release()

    # length = len(os.listdir(folder))
    print(video_url, "Done")

    return sorted(glob.glob(folder_path + "*.*"), key=lambda x: int(x.split("/")[-1].split(".")[0]))



def numpy_to_binary(arr):
    is_success, buffer = cv2.imencode(".jpg", arr)
    io_buf = io.BytesIO(buffer)
    return io_buf.read()


def get_detection_from_values(image_path):
    response = requests.post(api_path, files={"image": numpy_to_binary(image_path)}).json()
    return response

frame_timings = [[scene[0].get_seconds(), scene[1].get_seconds()] for scene in
                   detect(video_url, ContentDetector(), show_progress=True)]

frame_timings = sorted(frame_timings, key=lambda x: x[1] - x[0])
start_time, end_time = frame_timings[-1]
print(start_time, end_time, frame_timings)
# exit()

all_frames = extract_frame(video_url, start_time, end_time, frames_path)
overall_points = []
out_dict = {}
all_images = {}

for index, frame in enumerate(all_frames):
    img = cv2.imread(frame)
    all_images[frame] = img
    dets = get_detection_from_values(img)
    image_key = frame.split("/")[-1]
    out_image_key = crop_folder + image_key
    write_img = img

    if dets:
        selected = [max(dets, key=lambda x: x['confidence'])]
    else:
        selected = []

    hold_pts = []
    for det_i in selected:
        x1, y1, x2, y2, score = det_i['xmin'], det_i['ymin'], det_i['xmax'], det_i['ymax'], det_i['confidence'] * 100
        x1, y1, x2, y2 = list(map(int, [x1, y1, x2, y2]))
        overall_points.append(x1)
        if overall_points.count(x1) > 2: continue

        if score < 1: continue
        cv2.rectangle(write_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # cv2.putText(write_img, f'{score}-{x1}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
        #             1, (0, 0, 255), 3)
        hold_pts.append([x1, y1, x2, y2])

    objects = tracker.update(hold_pts)

    for (objectID, centroid) in objects.items():
        centroid = list(centroid)
        if objectID not in out_dict.keys():
            out_dict[int(objectID)] = [{'cord': list(map(int, centroid)), 'index': index + 1}]
        else:
            out_dict[int(objectID)].append({'cord': list(map(int, centroid)), 'index': index + 1})

        x1, y1 = centroid
        cv2.rectangle(write_img, (x1, y1), (x1 + 15, y1 + 10), (255, 0, 0), 2)
        cv2.putText(write_img, str(objectID), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2, cv2.LINE_AA, False)

        # print(objectID, centroid)
    cv2.imwrite(out_image_key, write_img)
    # print(f'Dets :: {dets}')

# print(f'Out dict :: {out_dict}', out_dict)
json.dump(out_dict, open('det_points4.json', 'w'))
# import allot_bounce_points




def find_distance(pt1, pt2):
    if pt1 and pt2:
        pt1 = np.array(pt1)
        pt2 = np.array(pt2)
        return np.linalg.norm(pt1 - pt2)
    print("returning 10000")
    return 10000

out_dict = json.load(open("det_points4.json","r"))


values_to_check = list(out_dict.values())
all_ids = list(out_dict.keys())

distance_sum = []
for id_i in all_ids:
    sum_i = []
    for index, pt_ in enumerate(out_dict[id_i][0: -1]):
        current_pt = pt_['cord']
        next_pt = out_dict[id_i][index + 1]['cord']
        distance = find_distance(current_pt, next_pt)
        sum_i.append(distance)

    distance_sum.append([id_i, sum(sum_i)])

input_pts_id = max(distance_sum, key=lambda x: x[1])[0]
print('MAX distance :: - ', distance_sum, input_pts_id)
input_pts = [i['cord'] for i in out_dict[input_pts_id]]

# firstAppearance = out_dict[input_pts_id][0]['index']
# firstAppearance = out_dict[input_pts_id][0]['index']

# print()