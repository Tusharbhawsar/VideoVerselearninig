import json, cv2, os, numpy as np, math, traceback
import centroidtracker
from scenedetect import detect, ContentDetector

from skspatial.objects import Circle, Line
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
from numpyencoder import NumpyEncoder
import uuid, requests



def find_distance( pt1, pt2):
    if pt1 and pt2:
        pt1 = np.array(pt1)
        pt2 = np.array(pt2)
        return np.linalg.norm(pt1 - pt2)
    return 10000


def testDecorator(testfun):

    def find_direction(circle_center, circle_radius, lineCords):
        x,y = lineCords[0]
        x2,y2 = lineCords[1]

        direction = [x-x2,y-y2]
        # return testfun(circle_center, circle_radius, lineCords[0],direction)
        return testfun(circle_center, circle_radius, (x,y),(x2,y2))

    return find_direction


@testDecorator
def find_circle_line_interection(circle_center, circle_radius, line_point1, line_point2):

    try:
        p = Point(circle_center[0],circle_center[1])
        c = p.buffer(circle_radius).boundary
        l = LineString([line_point1, line_point2])
        i = c.intersection(l)
        if i.geom_type == "LineString":
            return False
        return True
    except:
        return True




# from processPoints import detectAce
def getCentroid(boundingRect):
    xmin,ymin,xmax,ymax = boundingRect
    centroid = [(xmin+xmax)/2,(ymin+ymax)/2]
    return centroid
def checkIsInsideRect(boundingRect,cord):
    xmin,ymin,xmax,ymax = boundingRect
    # x_centroid, y_centroid = getCentroid(cord)
    x_centroid, y_centroid = cord
    if xmin<x_centroid<xmax and ymin<y_centroid<ymax:
        return True
    return False


def line(p1, p2):
    A = p1[1] - p2[1]
    B = p2[0] - p1[0]
    C = p1[0] * p2[1] - p2[0] * p1[1]
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return int(x), int(y)
    else:
        return False


def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

def angle_of_vectors( a, b, c, d):

    dotProduct = a * c + b * d
    # for three dimensional simply add dotProduct = a*c + b*d  + e*f
    modOfVector1 = math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d)
    # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f)
    angle = dotProduct / modOfVector1
    # print("Cosθ =",angle)
    angleInDegree = math.degrees(math.acos(angle))
    # print("θ =",angleInDegree,"°")
    return angleInDegree

def get_bounce_frame( ball_pos,bounce_threshold):
    index = 3
    angles = []
    old_a = None
    for i in range(index, len(ball_pos) - index):
        # print(i)

        if not old_a:
            a = ball_pos[i-index]
        else:
            # print(f"found old a using that {old_a}")
            a= old_a
        b = ball_pos[i]
        c = ball_pos[i+index]
        
        vector_1 = [b[0] - a[0], b[1] - a[1]]
        vector_2 = [c[0] - b[0], c[1] - b[1]]

        # print(vector_2)

        try:
            angle_1 = math.degrees(math.atan2(vector_1[0], vector_1[1]))
            angle_2 = math.degrees(math.atan2(vector_2[0], vector_2[1]))
            a, b = vector_1
            c, d = vector_2
            angle = angle_of_vectors(a, b, c, d)  # angle_2 -angle_1
            old_a = None
        except:
            # traceback.print_exc()
            if not old_a:
                old_a = ball_pos[i-index]
            angle = 0

        angle = abs(angle)

        if len(angles) > 3:

            if angle >= max(angles[-3::]) and angle < 250:

                for ii in range(-3, 0):
                    angles[ii] = 0
            else:
                angle = 0

        angles.append(angle)
    # bounce_frame = []
    # for k,j in enumerate(angles):
    #     if (j < 250 and j >=30 ):
    #         bounce_frame.append(k+index)
    # return bounce_frame
    bounce_frame = []
    turn_frame = []
    angles_index = []
    for k, j in enumerate(angles):
        if j <= 90 and j >= bounce_threshold:

            bounce_frame.append(k + index)
            angles_index.append({k+index : j})
        elif j > 90:
            turn_frame.append(k + index)
            angles_index.append({k+index : j})

    return bounce_frame, turn_frame, angles_index


def getLine( allLines):
    baseline_bottom = [
        int(allLines[8][0]),
        int(allLines[8][1]),
        int(allLines[11][0]),
        int(allLines[11][1]),
    ]
    baseline_top = [
        int(allLines[0][0]),
        int(allLines[0][1]),
        int(allLines[3][0]),
        int(allLines[3][1]),
    ]
    left_court_line = [
        int(allLines[0][0]),
        int(allLines[0][1]),
        int(allLines[8][0]),
        int(allLines[8][1]),
    ]
    right_court_line = [
        int(allLines[3][0]),
        int(allLines[3][1]),
        int(allLines[11][0]),
        int(allLines[11][1]),
    ]
    left_inner_line = [
        int(allLines[1][0]),
        int(allLines[1][1]),
        int(allLines[9][0]),
        int(allLines[9][1]),
    ]
    right_inner_line = [
        int(allLines[2][0]),
        int(allLines[2][1]),
        int(allLines[10][0]),
        int(allLines[10][1]),
    ]
    middle_line = [
        int(allLines[12][0]),
        int(allLines[12][1]),
        int(allLines[13][0]),
        int(allLines[13][1]),
    ]
    bottom_inner_line = [
        int(allLines[6][0]),
        int(allLines[6][1]),
        int(allLines[7][0]),
        int(allLines[7][1]),
    ]
    top_inner_line = [
        int(allLines[4][0]),
        int(allLines[4][1]),
        int(allLines[5][0]),
        int(allLines[5][1]),
    ]
    net = [
        int((allLines[0][0] + allLines[8][0]) / 2),
        int((allLines[6][1] + allLines[4][1]) / 2.15),
        int((allLines[3][0] + allLines[11][0]) / 2),
        int((allLines[5][1] + allLines[7][1]) / 2.15),
    ]
    # sortLines()
    (
        baseline_top,
        top_inner_line,
        bottom_inner_line,
        baseline_bottom,
    ) = sorted(
        [
            baseline_top,
            baseline_bottom,
            top_inner_line,
            bottom_inner_line,
        ],
        key=lambda x: x[1],
    )
    (
        left_court_line,
        left_inner_line,
        right_inner_line,
        right_court_line,
    ) = sorted(
        [
            left_court_line,
            right_court_line,
            left_inner_line,
            right_inner_line,
        ],
        key=lambda x: x[0],
    )
    return (
        baseline_top,
        baseline_bottom,
        left_court_line,
        right_court_line,
        left_inner_line,
        right_inner_line,
        middle_line,
        top_inner_line,
        bottom_inner_line,
        net,
    )




def check_for_lineTouching(ball_is_in_court,ballCenter):
    if ball_is_in_court == "TopLeft":
        if find_circle_line_interection(ballCenter,20,[top_inner_line[:2],top_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[left_inner_line[:2],left_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "BottomLeft":
        if find_circle_line_interection(ballCenter,20,[bottom_inner_line[:2],bottom_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[left_inner_line[:2],left_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "TopRight":
        if find_circle_line_interection(ballCenter,20,[top_inner_line[:2],top_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[right_inner_line[:2],right_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "BottomRight":
        if find_circle_line_interection(ballCenter,20,[bottom_inner_line[:2],bottom_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[right_inner_line[:2],right_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False


def drawCourt( image):
    cv2.line(image, baseline_top[:2], baseline_top[2:4], (0, 0, 255), 1)
    # cv2.line(frame,baseline_bottom[:2],baseline_bottom[2:4],(0,0,255),5)
    cv2.line(
        image, left_court_line[:2], left_court_line[2:4], (0, 0, 255), 1
    )
    cv2.line(
        image, right_court_line[:2], right_court_line[2:4], (0, 0, 255), 1
    )
    cv2.line(
        image, left_inner_line[:2], left_inner_line[2:4], (0, 0, 255), 1
    )
    cv2.line(
        image, right_inner_line[:2], right_inner_line[2:4], (0, 0, 255), 1
    )
    cv2.line(image, middle_line[:2], middle_line[2:4], (0, 0, 255), 1)
    cv2.line(
        image, top_inner_line[:2], top_inner_line[2:4], (0, 0, 255), 1
    )
    # cv2.line(frame,bottom_inner_line[:2],bottom_inner_line[2:4],(0,0,0),5)
    cv2.line(image, net[:2], net[2:4], (0, 0, 0), 1)


def destroy2ndBalls( balls):
    testBall = balls
    print(testBall[0])
    xs = [a[0] for a in testBall]
    minxs = min(xs)
    maxxs = max(xs)
    ys = [a[1] for a in testBall]
    minys = min(ys)
    maxys = max(ys)
    print(minxs, maxxs, minys, maxys)

    if (maxxs - minxs) < 200 and (maxys - minys) < 200:
        return True
    return False

def delete_notMoving( coords):
    # print(coords)
    coords = coords.copy()
    for i in range(len(coords) - 1):
        if coords[i] is not None and coords[i + 1] is not None:
            point1 = coords[i]
            point2 = coords[i + 1]
            diff = [abs(point2[0] - point1[0]), abs(point2[1] - point1[1])]

            if diff[0] < 5 and diff[1] < 5:
                coords[i] = None
    # print(coords)
    return coords
def getMovingBalls():
            
    print("*************************************************************************",ballDicts)
    for keys, value in ballDicts.items():
        print(
            "*************************************************************************",
            keys,
            "*************************************************************************",
        )
        # print(list(value.values()))
        newcords = delete_notMoving(list(value.values()))
        newCordsDict[keys] = {"cords": newcords}
        newCordsDict[keys].update({"indexes": list(value.keys())})
        for i in range(len(newcords) - 2):
            if newcords[i] is not None:
                if newcords[i + 1] is not None and newcords[i + 2] is not None:
                    # print(f":::::::::::::::::::::::::::::::{i} ......................{list(value.keys())},{list(value.values())},{newcords}")
                    newCordsDict[keys].update(
                        {"first_motion": list(value.keys())[i]}
                    )
                    break
        print(newCordsDict)
    return newCordsDict

def getOneTRajectofAll():

    actualBalls = []

    currentPoints = []
    lastPoints = []
    # print(newCordsDict)
    global firstAppearance
    firstAppearance = min(
        [
            x["first_motion"]
            for x in newCordsDict.values()
            if x.get("first_motion")
        ]
    )
    # print(
    #     firstAppearance,
    #     frame_n,
    #     ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::",
    # )
    for i in range(firstAppearance, stopFrame):
        for key, value in newCordsDict.items():
            # try:
            # print(i, key)
            try:
                currentPoints.append(value["cords"][value["indexes"].index(i)])
            except:
                currentPoints.append(None)

        if lastPoints:
            distList = [
                find_distance(x, y) for x, y in zip(currentPoints, lastPoints)
            ]
            seem2beTrue = currentPoints[distList.index(min(distList))]
            # if seem2beTrue is None:
            actualBalls.append(seem2beTrue)

        else:
            actualBalls.append([point for point in currentPoints if point][0])

        lastPoints = currentPoints
        currentPoints = []

    # for i, poss in enumerate(actualBalls):
    #     if poss and i > 100:
    #         print(i, poss)
    #         if not detection_boundary_poly.contains(Point(poss[0], poss[1])):
    #             actualBalls = actualBalls[:i]
    #             break

    return actualBalls












# def servicePoint( startingCourt,file_key = None):

#     uid = str(uuid.uuid4())
#     image_key_path = (
#         sagemaker_credentials["folder_path"] + uid + "/" + uid + ".jpg"
#     )
#     if not file_key:file_key = allImages[firstAppearance - startAt]

#     servicePos_upl.uploadFileOnS3_sync(file_key, image_key_path)
#     # if os.path.isdir(file_key): os.remove(file_key)
#     json_s3_key = sagemaker_credentials.get("cdn_suffix", "") + image_key_path
#     print(json_s3_key)

#     url = "https://zot6ryxvue.execute-api.ap-south-1.amazonaws.com/yolov5-small-global-detection"
#     payload = json.dumps({"image_path": json_s3_key})

#     headers = {"Content-Type": "application/json"}

#     response = requests.request("POST", url, data=payload)

#     # print(response.text)
#     persons_boxes = []
#     results = response.json()
#     print(results)
#     # testImg =cv2.imread(file_key)
#     for result in results["result"]:
#         print(result)
#         xmin, ymin, xmax, ymax = result["coordinates"]
#         conf, object_class = float(result["score"]), result["label"]
#         # xmin,ymin,xmax,ymax,conf,object_class = result["xmin"],result["ymin"],result["xmax"],result["ymax"],result["conf"], result["class"]
#         if object_class == "person":

#             if ymax < net[1] and min(net[0],net[2]) < (xmin + xmax) / 2 < max(net[0],net[2]):
#                 persons_boxes.append([xmin, ymin, xmax, ymax, conf])
#                 # cv2.rectangle(testImg,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,0,255),2)
#             else:
#                 if ymax > net[1]:
#                     persons_boxes.append([xmin, ymin, xmax, ymax, conf])
#                     # cv2.rectangle(testImg,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,0,255),2)
#     # cv2.circle(testImg,(int(net[0]),int(net[1])),4,(0,0,255),5)
#     # cv2.imshow("TESTIMAGE",testImg)
#     # cv2.waitKey(0)
#     playerss = getPlayers(persons_boxes)
#     print("playerss",playerss)
#     if len(playerss) == 2:
#         if startingCourt == "top":
#             xmin, ymin, xmax, ymax = playerss[0]
#             return (int((xmin + xmax) / 2), int(ymax))
#         else:
#             xmin, ymin, xmax, ymax = playerss[1]
#             return (int((xmin + xmax) / 2), int(ymax))
#     elif len(playerss) == 4:
#         if startingCourt == "top":
#             xmin, ymin, xmax, ymax = playerss[1]
#             return (int((xmin + xmax) / 2), int(ymax))
#         else:
#             xmin, ymin, xmax, ymax = playerss[2]
#             return (int((xmin + xmax) / 2), int(ymax))
#     else:
#         servicepoint = servicePoint(startingCourt,file_key = allImages[firstAppearance - startAt+5])
#         return servicepoint

def getTopPersons( persons, baseline):
    # print(persons, baseline)
    topPersons = []
    for xmin, ymin, xmax, ymax, conf in persons:
        if ymax < (net[1]):
            topPersons.append([xmin, ymin, xmax, ymax, conf])
    return topPersons

def getBottomPersons( persons, baseline):
    bottomPersons = []
    for xmin, ymin, xmax, ymax, conf in persons:
        if ymax > net[1]:
            bottomPersons.append([xmin, ymin, xmax, ymax, conf])
    return bottomPersons

def checkMatchType( personBoxes):
    personsInside = 0
    for xmin, ymin, xmax, ymax, conf in personBoxes:
        # if net[0]<(xmin+xmax)/2<net[2] and baseline_top[1]<(ymin+ymax)/2<baseline_bottom[3]:
        if net[0] < (xmin + xmax) / 2 < net[2] and (
            baseline_top[1] < ymax < baseline_bottom[3]
            or baseline_top[1] < (ymax + ymin) / 2 < baseline_bottom[3]
        ):
            # cv2.rectangle(court_frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,0,255),8)
            personsInside += 1

        if personsInside > 2:
            return "Doubles"

    else:
        return "Singles"

def y_dist_box_bottom( box, baseline):
    # print(box,baseline)
    if baseline[0] < (box[0] + box[2]) / 2 < baseline[2]:
        return abs(box[3] - baseline[1])
    else:
        return 5000

def getPlayers( persons_boxes):
    matchType = checkMatchType(persons_boxes)
    # if matchType =="Singles":
    #     print(f"{folderPath}/{file} is a Singles match")
    #     break
    tops = getTopPersons(persons_boxes, net)
    bottoms = getBottomPersons(persons_boxes, net)
    # print("tops::",tops)
    # print("bottoms::",bottoms)
    players = []
    player_probs = []

    if len(persons_boxes) > 0:
        if matchType == "Singles":
            # Choose person with biggest box
            # biggest_box = sorted(persons_boxes, key=lambda x: area_of_box(x), reverse=True)[0]
            # xmin,ymin,xmax,ymax = biggest_box
            try:
                sortedPersonsTop = sorted(
                    tops, key=lambda x: y_dist_box_bottom(x, net)
                )
                # print("sortedPersonsTop",sortedPersonsTop)
                # nearest_box_bottom,nearest_box_top = sorted(persons_boxes, key=lambda x: y_dist_box_bottom(x,net))[0]
                nearest_box_top = sortedPersonsTop[0]
                xmin, ymin, xmax, ymax, conf = nearest_box_top

                players.append([xmin, ymin, xmax, ymax])
                player_probs.append(conf)

                sortedPersonsBottom = sorted(
                    bottoms,
                    key=lambda x: y_dist_box_bottom(x, baseline_bottom),
                )
                nearest_box_bottom = sortedPersonsBottom[0]
                xmin, ymin, xmax, ymax, conf = nearest_box_bottom
                players.append([xmin, ymin, xmax, ymax])
                player_probs.append(conf)
                # print(sortedPersonsBottom,"sortedPersonsTop",sortedPersonsTop)

            except Exception as e:
                print("singles", e)

        else:
            try:
                sortedPersonsTop = sorted(
                    tops, key=lambda x: y_dist_box_bottom(x, net)
                )

                try:
                    nearest_box_top = sortedPersonsTop[0]
                    xmin, ymin, xmax, ymax, conf = nearest_box_top
                    players.append([xmin, ymin, xmax, ymax])
                    player_probs.append(conf)
                except:
                    print(traceback.print_exc())
                try:
                    nearest_box_top2 = sortedPersonsTop[1]
                    xmin, ymin, xmax, ymax, conf = nearest_box_top2
                    players.append([xmin, ymin, xmax, ymax])
                    player_probs.append(conf)
                except:
                    print(traceback.print_exc())

                sortedPersonsBottom = sorted(
                    bottoms,
                    key=lambda x: y_dist_box_bottom(x, baseline_bottom),
                )
                try:
                    nearest_box_bottom = sortedPersonsBottom[0]
                    xmin, ymin, xmax, ymax, conf = nearest_box_bottom
                    players.append([xmin, ymin, xmax, ymax])
                    player_probs.append(conf)
                except:
                    print(traceback.print_exc())
                try:
                    nearest_box_bottom2 = sortedPersonsBottom[1]
                    xmin, ymin, xmax, ymax, conf = nearest_box_bottom2
                    players.append([xmin, ymin, xmax, ymax])
                    player_probs.append(conf)
                except:
                    print(traceback.print_exc())

            except Exception as e:
                print("doubles", e)
    return players

# def plotTrajectory( ball, bounces):

#     # print(len(ball))
#     # x = gaussian_filter1d([i[0] for i in ball], 3)
#     # y = gaussian_filter1d([i[1] for i in ball], 3)

#     # ball = [[x[i], y[i]] for i in range(len(ball))]
#     os.mkdir(f"{folder}_processed") if not os.path.exists(
#         f"{folder}_processed"
#     ) else print("AlreadyCreatedFolder")

#     for index, bal in enumerate(ball, 1):
#         img = cv2.imread(
#             allImages[firstAppearance + index - startAt]
#         )
#         # if not math.isnan(bal[0]):
#         drawCourt(img)
#         if bal[0]:
#             position = getCoordinatePosition_4(bal)
#             # print(bal)
#             if index > 2:
#                 slope = getSlope(ball[:index])
#                 # print(slope,index)
#                 img[:150, :350] = [0, 0, 0]

#                 img = cv2.putText(
#                     img,
#                     str(slope),
#                     (100, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     (255, 255, 0),
#                 )
#             bal = list(map(int, bal))
#             if index in bounces:
#                 # print("HERERERERER",bounces,index)
#                 cv2.circle(img, (int(bal[0]), int(bal[1])), 10, (205, 45, 189), 10)
#                 waitkey = 1

#             else:
#                 cv2.circle(
#                     img, (int(bal[0]), int(bal[1])), 2, colorDict[position], 2
#                 )
#                 waitkey = 1
#             cv2.putText(
#                 img,
#                 str(index),
#                 (bal[0], bal[1]),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5,
#                 colorDict[position],
#             )

#         cv2.imshow("Frame", img)
#         cv2.waitKey(waitkey)
#         # full_path[f'{index}.jpg'] = list(bal)

#         cv2.imwrite(
#             f"{folder}_processed/img_lin{index}.jpg",
#             img,
#             [cv2.IMWRITE_JPEG_QUALITY, 100],
#         )
#     # print(ball, len(ball))
#     cv2.destroyAllWindows()

# def plotReferenceTrajectory( ball, bounces, turns):

#     # print(len(ball))
#     # x = gaussian_filter1d([i[0] for i in ball], 3)
#     # y = gaussian_filter1d([i[1] for i in ball], 3)

#     # ball = [[x[i], y[i]] for i in range(len(ball))]
#     os.mkdir(f"{folder}_processed") if not os.path.exists(
#         f"{folder}_processed"
#     ) else print("AlreadyCreatedFolder")
#     img = np.ones((1080, 1920, 3), np.uint8)
#     for index, bal in enumerate(ball, 0):
#         # img = cv2.imread(os.path.join(folder,allImages[firstAppearance+index-startAt]))
#         # if not math.isnan(bal[0]):
#         drawCourt(img)
#         if bal[0]:
#             position = getCoordinatePosition_4(bal)
#             # print(bal)
#             # if index > 2:
#             #     # slope = getSlope(ball[:index])
#             #     # print(slope,index)
#             #     # img[:150,:350] = [0,0,0]

#             #     img = cv2.putText(
#             #         img,
#             #         str(index),
#             #         (int(bal[0]), int(bal[1])),
#             #         cv2.FONT_HERSHEY_SIMPLEX,
#             #         0.5,
#             #         (255, 255, 0),
#             #     )
#             bal = list(map(int, bal))
#             if index in bounces:
#                 # print("HERERERERER",bounces,index)
#                 cv2.circle(img, (int(bal[0]), int(bal[1])), 10, (205, 45, 189), 10)
#                 # waitkey = 1

#             elif index in turns:
#                 cv2.circle(img, (int(bal[0]), int(bal[1])), 10, (0, 0, 145), 10)

#             else:
#                 cv2.circle(
#                     img, (int(bal[0]), int(bal[1])), 2, colorDict[position], 2
#                 )
#                 # waitkey = 1
#             # cv2.putText(img, str(index), (bal[0], bal[1]), cv2.FONT_HERSHEY_SIMPLEX, .5,  colorDict[position])

#         # cv2.imshow("Frame",img)
#         # cv2.waitKey(waitkey)

#         # full_path[f'{index}.jpg'] = list(bal)

#     cv2.imwrite(
#         f"{folder}_processed/img_lin{uid}.jpg",
#         img,
#         [cv2.IMWRITE_JPEG_QUALITY, 100],
#     )
#     # print(ball, len(ball))
    # cv2.destroyAllWindows()

# def storeResults():
#     processed = {
#         "balldicts": ballDicts,
#         "newBallDicts": newCordsDict,
#         "oneTrack": actualBalls,
#         "interpolatedBalls": interpolation(actualBalls),
#         "polyInterp": getSmoothedTrajectory(),
#     }
#     jsonfile = json.dumps(processed)

#     with open(f"{folder}_cords.json", "w") as file:
#         file.write(jsonfile)

def getPosition( cords, lastposition):
    Position = None
    x_cord, y_cord = cords
    print(cords,(net[1], top_inner_line[1]),left_court_line,right_court_line)
    if (
        left_court_line[0] < x_cord < right_court_line[0]
        and y_cord < (net[1] + top_inner_line[1]) / 2
    ):
        Position = "top"
    else:
        Position = "bottom"

    return Position

def getstartingCourt( smoothTrack):
    xDir, yDir = getDirection(smoothTrack[:4])

    if yDir == "Down":
        return "bottom"
    else:
        return "top"

def getCourt( pos):
    point = Point(pos[0], pos[1])
    if top_court_boundary_poly.contains(point):
        return "top"
    elif bottom_court_boundary_poly.contains(point):
        return "bottom"
    else:
        return "out"

def check_service_or_track( smoothTRack):
    servicePath = [["bottom","top","bottom","top","out"],["bottom","top","out"]]

    trackPath = ["bottom","out"]

    positions = [getCourt(cords) for cords in smoothTRack]

    path = [positions[0]]
    # _ = [path.append(pos) for pos in positions if pos not in path]
    _ = [path.append(pos) for pos in positions if pos != path[-1]]

    print(path,positions)

    # if path in servicePath:
    #     return "service"
    # if path in trackPath:
    #     return "track"

    for pattern in servicePath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("service TRUE")
                return "service"
            else:
                print("False")
    for pattern in trackPath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("TRUE")
                return "track"
            else:
                print("False")

def check_service_or_track_4out( smoothTRack):
    servicePath = [["out","top","bottom","out"]]
    trackPath = ["out"]
    positions = [getCourt(cords) for cords in smoothTRack]

    path = [positions[0]]
    # _ = [path.append(pos) for pos in positions if pos not in path]
    _ = [path.append(pos) for pos in positions if pos != path[-1]]

    print(path,positions)

    # if path in servicePath:
    #     return "service"
    # if path in trackPath:
    #     return "track"

    for pattern in servicePath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("service TRUE")
                return "service"
            else:
                print("False")
    for pattern in trackPath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("TRUE")
                return "track"
            else:
                print("False")

def check_service_or_track_4top( smoothTRack):
    servicePath = [["top","bottom","out"]]
    trackPath = [["top","out"],["top","bottom","top","out"]]

    positions = [getCourt(cords) for cords in smoothTRack]

    path = [positions[0]]
    # _ = [path.append(pos) for pos in positions if pos not in path]
    _ = [path.append(pos) for pos in positions if pos != path[-1]]

    print(path,positions)

    # if path in servicePath:
    #     return "service"
    # if path in trackPath:
    #     return "track"

    for pattern in servicePath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("service TRUE")
                return "service"
            else:
                print("False")
    for pattern in trackPath:
        if len(path)>=len(pattern):
            if path[:len(pattern)]==pattern:
                print("TRUE")
                return "track"
            else:
                print("False")

def get_service_index(balls):
    directions = []
    dists = []
    ball_movemnts = []

    print(len(balls))


    dirTRavelled = []
    avgMoments = []

    for i in range(3,len(balls)):
        dir,dx,dy = getDirection(balls[i-3:i])
        ball_dist = find_distance(balls[i],balls[i-1])
        dists.append(dir)
        # if dir not in dirTRavelled:
        dirTRavelled.append(dir)

        directions.append([dx,dy])
        ball_movemnts.append(ball_dist)

        avgMoments.append(sum(ball_movemnts[i-3:i])/min(3,i-2))

    # print(ball_movemnts)
    # print(avgMoments)
    movement = []
    lastdir = ""
    lastdircount = 0
    for i,dir in enumerate(dirTRavelled):
        if len(dir)>0 and lastdir=="":
            lastdir = dir
            lastdircount+=1
        if lastdir==dir:
            lastdircount+=1
        else:
            if lastdircount>5:
                if movement and list(movement[-1].keys())[-1]!=lastdir:
                    movement.append({lastdir:i})
                if len(movement)<1:
                    movement.append({lastdir:i})
            lastdir = dir
            lastdircount=0



    serviceIndex = list(movement[1].values())[0]

    minxb4service = min([x for x,y in balls[:serviceIndex]])
    maxxb4service = max([x for x,y in balls[:serviceIndex]]) 
    minyb4service = min([y for x,y in balls[:serviceIndex]])
    maxyb4service = max([y for x,y in balls[:serviceIndex]]) 


    x_travelled = abs(maxxb4service-minxb4service)
    y_travelled = abs(maxyb4service-minyb4service)

    if x_travelled<250 and y_travelled<600:
        if minyb4service<baseline_top[1]:
            return 0
        return list(movement[1].values())[0]        
    return 0

def find_bounceThreshold(ball_track):
    courtList = [all_court_boundary_poly.contains(Point(pos[0],pos[1])) for pos in ball_track]
    courtList
    movement = []
    lastCourt = ""
    lastCourtcount = 0
    for i,Court in enumerate(courtList):
        if lastCourt==Court:
            lastCourtcount+=1
        else:
            if lastCourtcount>5:
                if movement and list(movement[-1].keys())[-1]!=lastCourt:
                    movement.append({lastCourt:i})
                if len(movement)<1:
                    movement.append({lastCourt:i})
            lastCourt = Court
            lastCourtcount=0
    print(movement)


    [list(movement.values())[0]for movement in movement]
    right_limit = (net_cross_middle[0]+net_cross_right_inner[0])/2
    # right_limit
    left_limit = (net_cross_middle[0]+net_cross_left_inner[0])/2
    # left_limit

    min(ball_track,key = lambda x:x[0])
    max(ball_track,key = lambda x:x[0])
    if min(ball_track,key = lambda x:x[0])[0]>left_limit and max(ball_track,key = lambda x:x[0])[0]<right_limit:
        print("threshold bounce angle will be 5degree")
        return 5
    else:
        return 15

def getCoordinateServicePosition_4( point):
    x, y = point
    position = None
    if x and y:
        if x < middle_line[0]:
            if y < net[1]:
                position = "TopLeft"
            else:
                position = "BottomLeft"
        else:
            if y < net[1]:
                position = "TopRight"
            else:
                position = "BottomRight"

    return position

def check_for_lineTouching(ball_is_in_court,ballCenter):
    if ball_is_in_court == "TopLeft":
        if find_circle_line_interection(ballCenter,20,[top_inner_line[:2],top_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[left_inner_line[:2],left_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "BottomLeft":
        if find_circle_line_interection(ballCenter,20,[bottom_inner_line[:2],bottom_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[left_inner_line[:2],left_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "TopRight":
        if find_circle_line_interection(ballCenter,20,[top_inner_line[:2],top_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[right_inner_line[:2],right_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

    if ball_is_in_court == "BottomRight":
        if find_circle_line_interection(ballCenter,20,[bottom_inner_line[:2],bottom_inner_line[2:]]) or \
            find_circle_line_interection(ballCenter,20,[right_inner_line[:2],right_inner_line[2:]]) or \
                find_circle_line_interection(ballCenter,20,[middle_line[:2],middle_line[2:]]):
            return True
        else:
            return False

def getCoordinatePosition_4( point):
    # x,y = point
    # print(point)
    point = Point(point[0], point[1])
    # print(point,topLeft_box_poly)
    position = "out"
    # if x and y:
    #     if left_inner_line[0]<x<middle_line[0]:
    #         if top_inner_line[1]<y<net[1]:
    #             position = "TopLeft"
    #         elif bottom_inner_line[1]>y>net[1]:
    #             position = "BottomLeft"
    #         else:
    #             position = "out"
    #     elif net[0]<x<right_inner_line[0]:
    #         if top_inner_line[1]<y<net[1]:
    #             position = "TopRight"
    #         elif bottom_inner_line[1]<y<net[1]:
    #             position = "BottomRight"
    #         else:
    #             position = "out"
    if topLeft_box_poly.contains(point):
        position = "TopLeft"
        # print(position,"????????????????????????????????",point)
    if topRight_box_poly.contains(point):
        position = "TopRight"
        # print(position,"????????????????????????????????",point)

    if bottomRight_box_poly.contains(point):
        position = "BottomRight"
        # print(position,"????????????????????????????????",point)
    if bottomLeft_box_poly.contains(point):
        position = "BottomLeft"
        # print(position,"????????????????????????????????",point)

    return position

def detectCourt( frame):
    print("Detecting the court and the players...")
    # lines = court_detector.detect(frame)
    # _, img_encoded = cv2.imencode('.jpg',frame)
    _, img_encoded = cv2.imencode(".jpg", frame)

    file = {"image": img_encoded.tobytes()}
    # file = {'image':frame}
    response = requests.post(url, files=file)

    print(response.json())
    lines = response.json()
    (
        baseline_top,
        baseline_bottom,
        left_court_line,
        right_court_line,
        left_inner_line,
        right_inner_line,
        middle_line,
        top_inner_line,
        bottom_inner_line,
        net,
    ) = getLine(lines)

    print("lines detected........")
    return (
        baseline_top,
        baseline_bottom,
        left_court_line,
        right_court_line,
        left_inner_line,
        right_inner_line,
        middle_line,
        top_inner_line,
        bottom_inner_line,
        net,
    )



def servicePoint( startingCourt,file_key = None):

    # # print(response.text)
    persons_boxes = []

    startAt = startFrame
    # if str(file_key.split('/')[-1].split('.')[0]) not in person_indexes: 
    if str(int(startFrame)+1) in person_indexes:
        persons = person_data[str(int(startFrame)+1)]
        for person in persons:
            if person:
                xmin,ymin,xmax,ymax,conf,object_class = int(person["xmin"]),int(person["ymin"]),int(person["xmax"]),int(person["ymax"]),person["confidence"], person["name"]
                # cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,255),2)

                if ymax < net[1] and min(net[0],net[2]) < (xmin + xmax) / 2 < max(net[0],net[2]):
                    persons_boxes.append([xmin, ymin, xmax, ymax, conf])
                    # cv2.rectangle(testImg,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,0,255),2)
                else:
                    if ymax > net[1]:
                        persons_boxes.append([xmin, ymin, xmax, ymax, conf])

    playerss = getPlayers(persons_boxes)
    print("playerss",playerss)
    if len(playerss) == 2:
        if startingCourt == "top":
            xmin, ymin, xmax, ymax = playerss[0]
            return (int((xmin + xmax) / 2), int(ymax))
        else:
            xmin, ymin, xmax, ymax = playerss[1]
            return (int((xmin + xmax) / 2), int(ymax))
    elif len(playerss) == 4:
        if startingCourt == "top":
            xmin, ymin, xmax, ymax = playerss[1]
            return (int((xmin + xmax) / 2), int(ymax))
        else:
            xmin, ymin, xmax, ymax = playerss[2]
            return (int((xmin + xmax) / 2), int(ymax))
    else:
        servicepoint = servicePoint(startingCourt,file_key = startAt+5)
        print(videoName)
        return servicepoint
        # return (None,None)



def finalTrackFilter():
    # ballDicts = {}
    frame_n=0
    # if frame_n<startFrame or frame_n>stopFrame: continue
    for i in range(len(ball_indexes)):
        frame_n+=1
        if str(frame_n) in ball_indexes:
            balls = ball_data[str(frame_n)]
            current_frame_balls = []
            for ball in balls:
                if ball:
                    xmin,ymin,xmax,ymax,conf,object_class = int(ball["xmin"]),int(ball["ymin"]),int(ball["xmax"]),int(ball["ymax"]),ball["confidence"], ball["name"]
                    if conf < .65: continue

                    # cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,0,255),2)
                    current_frame_balls.append([xmin,ymin,xmax,ymax])

            objects = tracker.update(current_frame_balls)
            for (objectID, centroid) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "ID {}".format(objectID)
                # cv2.putText(
                #     frame,
                #     text,
                #     (centroid[0] - 10, centroid[1] - 10),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     0.5,
                #     (0, 255, 0),
                #     2,
                # )
                # cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

                if objectID in ballDicts.keys():
                    ballDicts[objectID].update(
                        {frame_n: centroid.tolist()}
                    )
                else:
                    ballDicts[objectID] = {frame_n: centroid.tolist()}

    ballIDs = list(ballDicts.keys())
    # print("///////////////////////////",ballDicts)
    for i in ballIDs:
        # print(ballDicts[i])
        if destroy2ndBalls(list(ballDicts[i].values())):
            del ballDicts[i]

    ballsMovingPoint = getMovingBalls()
    print(ballsMovingPoint)
    oneTrack = getOneTRajectofAll()
    print(oneTrack)
    smoothTRack = []
    _ = [smoothTRack.append(pos) if pos else smoothTRack.append(smoothTRack[-1]) for pos in oneTrack ]
    # oneTrack = smoothTRack


    return smoothTRack





# https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/PJISwos4B/1676971603.mp4
# links = ["https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/PJISwos4B/1676971603.mp4"]#,"https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/PJISwos4B/1676971529.mp4"]
import glob
links = glob.glob("/home/multi-sy-008/videoverse/tennis_utils/match_8/*.mp4")
url = "http://0.0.0.0:8017/v1/court-detection/LETR"
links = ["/home/multi-sy-008/videoverse/tennis_utils/match_1/match_12_0_03_58.mp4"]
links = ["https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173379.mp4"]
links = ["https://d1zxk9teuo4ijt.cloudfront.net/15ytizwDs/1676355022.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/KWyBBchfX/1676354948.mp4",
"https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530790.mp4",
"https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530857.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035068.mp4"]
for link in links[0:]:
    newCordsDict = {}

    try:
        print(link)
        saveFolder = link.split("/")[-1].split(".")[0]
        if os.path.exists(saveFolder) :print("ALERESDFSSD") 
        else: os.mkdir(saveFolder)
        jsonFolderPath = "/home/multi-sy-008/Downloads/testModelv5/jsonfiles"

        # ball_json = "/home/multi-sy-008/Downloads/testModelv5/1676971603/1676971603_ball.json"
        # person_json = "/home/multi-sy-008/Downloads/testModelv5/1676971603/1676971603_person.json"
        # racket_json = "/home/multi-sy-008/Downloads/testModelv5/1676971603/1676971603_racket.json"

        # jsonFolderPath = "/home/multi-sy-008/videoverse/tennis_utils/jsonfiles"
        videoName = link.split('/')[-1]
        ball_json = f"{jsonFolderPath}/{videoName.split('.')[0]}_ball.json"
        person_json = f"{jsonFolderPath}/{videoName.split('.')[0]}_person.json"
        racket_json = f"{jsonFolderPath}/{videoName.split('.')[0]}_racket.json"

        lines = [[411, 738, 1], [546, 738, 1], [1364, 738, 1], [1502, 738, 1], [611, 583, 1], [1296, 582, 1], [703, 364, 1], [1199, 362, 1], [655, 303, 1], [728, 303, 1], [1172, 301, 1], [1247, 301, 1], [952, 583, 1], [950, 363, 1]]
        # lines = [[324, 775, 1], [481, 775, 1], [1431, 776, 1], [1590, 776, 1], [556, 599, 1], [1359, 599, 1], [664, 345, 1], [1254, 343, 1], [607, 273, 1], [695, 272, 1], [1225, 271, 1], [1313, 271, 1], [956, 599, 1], [959, 344, 1]]
        # (
        #     baseline_top,
        #     baseline_bottom,
        #     left_court_line,
        #     right_court_line,
        #     left_inner_line,
        #     right_inner_line,
        #     middle_line,
        #     top_inner_line,
        #     bottom_inner_line,
        #     net,
        # ) = detectCourt(frame)
        with open (ball_json,'r') as balls:
            ball_data = json.loads(json.load(balls))
            ball_indexes = list(ball_data.keys())

        with open (person_json,'r') as persons:
            person_data = json.loads(json.load(persons))
            person_indexes = list(person_data.keys())

        with open (racket_json,'r') as rackets:
            racket_data = json.loads(json.load(rackets))
            racket_indexes = list(racket_data.keys())

        distanceDict = {}
        # print(f"balls \t {ball_data} \n persons \t {person_data} \n rackets \t {racket_data} \n ")
        aceCourtDict = {
            "TopLeft": "BottomRight",
            "BottomLeft": "TopRight",
            "TopRight": "BottomLeft",
            "BottomRight": "TopLeft",
        }



        jsonResultFile = {}
        ballDicts = {}
        tracker = centroidtracker.CentroidTracker()
        video = cv2.VideoCapture(link)

        time_frames = max(
            [
                [scene[0].get_seconds(), scene[1].get_seconds()]
                for scene in detect(link, ContentDetector())
            ],
            key=lambda x: x[1] - x[0],
        )

        startTime, stopTime = time_frames
        fps = 50
        startFrame, stopFrame = int(startTime * fps), int(stopTime * fps)

        video.set(1,(startFrame+stopFrame)/2)
        ret,frame = video.read()

        (baseline_top,
        baseline_bottom,
        left_court_line,
        right_court_line,
        left_inner_line,
        right_inner_line,
        middle_line,
        top_inner_line,
        bottom_inner_line,
        net) = detectCourt(frame)    #= getLine(lines)
        # net) = getLine(lines)
        video.set(1,0)
        # (
        #     topLeft_box_poly,
        #     topRight_box_poly,
        #     bottomLeft_box_poly,
        #     bottomRight_box_poly,
        #     top_court_boundary_poly,
        #     bottom_court_boundary_poly

        # ) = get_Boxes()


        baseline_top___ = line(baseline_top[0:2], baseline_top[2:4])
        baseline_bottom___ = line(baseline_bottom[0:2], baseline_bottom[2:4])
        left_court_line___ = line(left_court_line[0:2], left_court_line[2:4])
        right_court_line___ = line(
            right_court_line[0:2], right_court_line[2:4]
        )
        left_inner_line___ = line(left_inner_line[0:2], left_inner_line[2:4])
        right_inner_line___ = line(
            right_inner_line[0:2], right_inner_line[2:4]
        )
        middle_line___ = line(middle_line[0:2], middle_line[2:4])
        top_inner_line___ = line(top_inner_line[0:2], top_inner_line[2:4])
        bottom_inner_line___ = line(
            bottom_inner_line[0:2], bottom_inner_line[2:4]
        )
        net___ = line(net[0:2], net[2:4])
        top_inner_cross_left_inner = list(
            intersection(top_inner_line___, left_inner_line___)
        )
        top_inner_cross_middle = list(intersection(top_inner_line___, middle_line___))
        top_inner_cross_right_inner = list(
            intersection(top_inner_line___, right_inner_line___)
        )
        bottom_inner_cross_left_inner = list(
            intersection(bottom_inner_line___, left_inner_line___)
        )
        bottom_inner_cross_middle = list(
            intersection(bottom_inner_line___, middle_line___)
        )
        bottom_inner_cross_right_inner = list(
            intersection(bottom_inner_line___, right_inner_line___)
        )
        net_cross_left_inner = list(intersection(net___, left_inner_line___))
        net_cross_middle = list(intersection(net___, middle_line___))
        net_cross_right_inner = list(intersection(net___, right_inner_line___))

        topLeft_box = [
            top_inner_cross_left_inner,
            top_inner_cross_middle,
            net_cross_middle,
            net_cross_left_inner,
        ]
        topRight_box = [
            top_inner_cross_middle,
            top_inner_cross_right_inner,
            net_cross_right_inner,
            net_cross_middle,
        ]
        bottomLeft_box = [
            net_cross_left_inner,
            net_cross_middle,
            bottom_inner_cross_middle,
            bottom_inner_cross_left_inner,
        ]
        bottomRight_box = [
            net_cross_middle,
            net_cross_right_inner,
            bottom_inner_cross_right_inner,
            bottom_inner_cross_middle,
        ]

        all_court_boundary = [
            list(
            intersection(baseline_top___, left_court_line___)
        ),
            list(
            intersection(baseline_top___, right_court_line___)
        ),
            list(
            intersection(baseline_bottom___, right_court_line___)
        ),
            list(
            intersection(baseline_bottom___, left_court_line___)
        ),
        ]

        all_court_boundary_poly = Polygon(all_court_boundary)
        topLeft_box_poly = Polygon(topLeft_box)
        topRight_box_poly = Polygon(topRight_box)
        bottomLeft_box_poly = Polygon(bottomLeft_box)
        bottomRight_box_poly = Polygon(bottomRight_box)

        bottom_court_boundary = [
            net[0:2],
            net[2:4],
            baseline_bottom[2:4],
            baseline_bottom[0:2],
        ]
        top_court_boundary = [
            net[0:2],
            net[2:4],
            baseline_top[2:4],
            baseline_top[0:2],
        ]
        top_court_boundary_poly = Polygon(top_court_boundary)
        bottom_court_boundary_poly = Polygon(bottom_court_boundary)
        print(
            bottom_court_boundary,
            top_court_boundary,
            top_court_boundary_poly,
            bottom_court_boundary_poly,
        )
        # return (
        #     topLeft_box_poly,
        #     topRight_box_poly,
        #     bottomLeft_box_poly,
        #     bottomRight_box_poly,
        #     top_court_boundary_poly,
        #     bottom_court_boundary_poly
        # )




        # video = cv2.VideoCapture("/home/multi-sy-008/Nick Kyrgios is a born entertainer 😂  _ His funniest moments and greatest shots at Wimbledon-5K-BBhe4-ew.mp4")
        frame_n = 0
        saveFolder = link.split("/")[-1].split(".")[0]
        if os.path.exists(saveFolder) :print("ALERESDFSSD") 
        else: os.mkdir(saveFolder)

        oneTrack = smoothTRack = finalTrackFilter()

        print(smoothTRack)
        while video.isOpened():
            frame_n+=1
            ret, frame = video.read()
            if ret:
                c_h,c_w,_ = frame.shape

                if frame_n<startFrame or frame_n>stopFrame: continue
                if str(frame_n) in ball_indexes:
                    balls = ball_data[str(frame_n)]
                    current_frame_balls = []
                    for ball in balls:
                        if ball:
                            xmin,ymin,xmax,ymax,conf,object_class = int(ball["xmin"]),int(ball["ymin"]),int(ball["xmax"]),int(ball["ymax"]),ball["confidence"], ball["name"]
                            if conf < .65: continue
                            cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,0,255),2)
                            current_frame_balls.append([xmin,ymin,xmax,ymax])

                    objects = tracker.update(current_frame_balls)
                    for (objectID, centroid) in objects.items():
                        # draw both the ID of the object and the centroid of the
                        # object on the output frame
                        text = "ID {}".format(objectID)
                        cv2.putText(
                            frame,
                            text,
                            (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )
                        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        
                        if objectID in ballDicts.keys():
                            ballDicts[objectID].update(
                                {frame_n: centroid.tolist()}
                            )
                        else:
                            ballDicts[objectID] = {frame_n: centroid.tolist()}

                persons_boxes = []
                if str(frame_n) in person_indexes:
                    persons = person_data[str(frame_n)]
                    for person in persons:
                        if person:
                            xmin,ymin,xmax,ymax,conf,object_class = int(person["xmin"]),int(person["ymin"]),int(person["xmax"]),int(person["ymax"]),person["confidence"], person["name"]
                            cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,255),2)
                            persons_boxes.append([xmin,ymin,xmax,ymax,conf])
                
                
                if str(frame_n) in racket_indexes:
                    rackets = racket_data[str(frame_n)]
                    for racket in rackets:
                        if racket:
                            xmin,ymin,xmax,ymax,conf,object_class = int(racket["xmin"]),int(racket["ymin"]),int(racket["xmax"]),int(racket["ymax"]),racket["confidence"], racket["name"]
                            cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(255,0,255),2)
                    

                if stopFrame> frame_n>firstAppearance and smoothTRack[frame_n -firstAppearance -1][1]<top_inner_line[1]:
                    players = getPlayers(persons_boxes)
                    if players:
                        players = min(players , key=lambda x :x[1])
                        print(players)

                        print(len(smoothTRack),(frame_n -firstAppearance ),frame_n,firstAppearance ,int(startFrame))
                        xmin,ymin,xmax,ymax = players
                        personBallDistance = find_distance(smoothTRack[frame_n -firstAppearance -1],getCentroid([xmin,ymin,xmax,ymax]))
                        cv2.putText(frame,str(personBallDistance),(xmin,ymin-10),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,2,255),2)
                        cv2.circle(frame,smoothTRack[frame_n -firstAppearance -1],5,(200,0,200),5)
                        distanceDict.update({frame_n:{"ballCord":smoothTRack[frame_n -firstAppearance -1],"playerCord":[xmin,ymin,xmax,ymax],"distance":personBallDistance}})
                        cv2.circle(frame,list(map(int,getCentroid([xmin,ymin,xmax,ymax]))),5,(0,0,200),5)


                # frame+=100
                drawCourt(frame)

                cv2.imshow("FRAME",frame)
                cv2.imwrite(f"{saveFolder}/{frame_n}.jpg",frame)

                cv2.waitKey(1)



            else:
                print(distanceDict)
                distList = [[key,value['distance']] for key,value in distanceDict.items()]
                minindex = min(distList, key = lambda x:x[1])
                # minindex
                yminIndex = min([[key,value['ballCord']] for key,value in distanceDict.items()], key = lambda x:x[1])

                



                break

        


        print("oneTrack::", oneTrack)
        img = np.ones((1080,1920,3),np.uint8())
        tr = 0
        for pos in smoothTRack:
            if pos:
                pos = list(map(int,pos))
                # cv2.circle(img,pos,1,(0,0,200),1)
                cv2.putText(img,f"{tr}",(pos),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,2,255),1)
                tr+=1

        bounces,turns,angle_index = get_bounce_frame(smoothTRack,5)

        for bounc in bounces:
            # print(smoothTRack[bounc])
            pos = list(map(int,smoothTRack[bounc]))
            cv2.circle(img,pos,3,(255,255,200),3)
        for turn in turns:
            # print(smoothTRack[turn])
            pos = list(map(int,smoothTRack[turn]))
            cv2.circle(img,pos,4,(100,100,200),4)

        print(f"angle_index:: {angle_index}")
        print(bounces,turns)
        drawCourt(img)
        cv2.imshow("img",img)
        cv2.waitKey(1)




        video.release()
    except:
        video.release()

        # cv2.destroyAllWindows()

        traceback.print_exc()


    