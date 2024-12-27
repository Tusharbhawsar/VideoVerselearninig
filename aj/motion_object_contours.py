import json
import centroidtracker
import cv2
from scenedetect import detect, ContentDetector
import numpy as np

video_url = "1675173497.mp4"

cap = cv2.VideoCapture(video_url)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter("output.mkv", fourcc, 5.0, (1920, 1070))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

time_frames = max([[scene[0].get_seconds(), scene[1].get_seconds()] for scene in
                   detect(video_url, ContentDetector(), show_progress=True)],
                  key=lambda x: x[1] - x[0])
start_time, end_time = time_frames
start_time = 66 #start_time * 50
end_time = end_time * 50
frame_count = 1
print(start_time, end_time)
print(frame1.shape)


def find_distance(pts, compare_points):
    dist = np.linalg.norm(np.array(pts) - np.array(compare_points))
    return dist
    # printing Euclidean distance


out_dict = {}
tracker = centroidtracker.CentroidTracker()
out_folder = "motion_contour/"
all_pre_points = [[906, 635], [907, 622], [906, 612], [906, 601], [906, 591], [907, 581], [907, 571], [906, 562], [906, 554], [906, 545], [906, 538], [906, 530], [906, 523], [906, 516], [906, 510], [906, 505], [906, 499], None, [907, 490], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, [911, 490], [910, 495], [911, 500], [911, 506], [912, 512], [912, 518], [924, 514], [943, 500], [983, 474], [999, 463], [1020, 451], [1037, 439], None, None, None, None, None, [1059, 426], [1142, 378], [1152, 374], [1162, 370], [1171, 366], [1179, 363], [1187, 354], [1193, 333], [1200, 313], None, None, None, [1204, 298], [1228, 239], [1233, 226], [1237, 216], [1242, 206], [1246, 196], [1250, 187], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, [1120, 223], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
pre_done = 0
last_result = all_pre_points[0]

while cap.isOpened():
    frame_count += 1
    # frame1 = frame1[257: 832, 591: 1260]
    # frame2 = frame2[257: 832, 591: 1260]

    file_key = str(frame_count) + ".jpg"
    try:
        diff = cv2.absdiff(frame1, frame2)
    except:
        break

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if start_time < frame_count < end_time:

        det = []

        print(f'Area to find is {frame_count} {all_pre_points[pre_done]} ')

        cdpp = all_pre_points[pre_done]

        if not cdpp:
            temp_cdpp = last_result
            actual_w, acutal_h = temp_cdpp
            # cv2.rectangle(frame1, (temp_cdpp[0] - 10, temp_cdpp[1] - 10), (temp_cdpp[0] + 10, temp_cdpp[1] + 10), (0, 255, 0), 2)
            # cv2.putText(frame1, f'Raw', (temp_cdpp[0], temp_cdpp[1]), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (0, 0, 255), 3)

            all_contours = []
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                contour_area = cv2.contourArea(contour)
                all_contours.append([x, y, w, h])
                # if 130 > h > 10:
                #     if 10 < w < 40:
                #         det.append([x, y, x + w, y + h])
                # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                #             1, (0, 0, 255), 3)
                # cv2.putText(frame1, f'{w}-{h}', (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX,
                #             1, (0, 0, 255), 3)

            closer = min([[find_distance(temp_cdpp, i[0:2]), i] for i in all_contours], key=lambda x: x[0])
            print('Closer :: ', closer)
            x, y, w, h = closer[1]
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
            cv2.putText(frame1, f'{w}-{h}', (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
            det.append([x, y, x + w, y + h])
        else:
            temp_cdpp = cdpp
            actual_w, acutal_h = temp_cdpp
            cv2.rectangle(frame1, (temp_cdpp[0] - 10, temp_cdpp[1] - 10), (temp_cdpp[0] + 10, temp_cdpp[1] + 10),
                          (255, 255, 0), 2)
            cv2.putText(frame1, f'Raw', (temp_cdpp[0], temp_cdpp[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
            det.append([actual_w, acutal_h, actual_w + 10, acutal_h + 10])

        if cdpp:
            last_result = cdpp
        else:
            last_result = [x, y]

        objects = tracker.update(det)
        for (objectID, centroid) in objects.items():
            centroid = list(centroid)
            if objectID not in out_dict.keys():
                out_dict[objectID] = [{'cord': centroid, 'index': file_key}]
            else:
                out_dict[objectID].append({'cord': centroid, 'index': file_key})

            # print(objectID, centroid)
            x1, y1 = centroid
            # cv2.rectangle(frame1, (x1, y1), (x1 + 15, y1 + 10), (255, 0, 0), 2)
            # cv2.putText(frame1, str(objectID), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
            #                    (0, 0, 255), 2, cv2.LINE_AA, False)
        else:
            cv2.imwrite(out_folder + file_key, frame1)

        pre_done += 1

    if start_time < frame_count + 1 < end_time: out.write(frame1)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()

print(f'total frame count :: {frame_count}')
