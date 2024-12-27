import cv2
import json
import requests
from numpyencoder import NumpyEncoder
import glob
url_person = "http://0.0.0.0:5002//v1/object-detection/yolov5s"
url_ball = "http://0.0.0.0:5002//v1/object-detection/yolov5s2"
url_racket = "http://0.0.0.0:5002//v1/object-detection/yolov5s3"



import os


# videoUrl  = "https://d1zxk9teuo4ijt.cloudfront.net/Y-NSrzbhz/1675150480.mp4"

# video = cv2.VideoCapture(videoUrl)
# frameNu = 0
# print(video.isOpened())
# while video.isOpened():
#     ret,frame = video.read()
#     if not ret:
#         break
#     cv2.imwrite("/home/multi-sy-008/Downloads/testModelv5/tesFrame564/"+str(frameNu)+".jpg",frame)
#     frameNu +=1

# video.release()


print("herererere")

    

with open("/home/multi-sy-008/videoverse/tracknetTestData/oldAceClassifiedData/Match_11_march_10.txt","r") as csss:
    rows = csss.readlines()




# with open("/home/multi-sy-008/videoverse/tracknetTestData/newTest.txt","r") as csss:
#     rows = csss.readlines()


# rows = ["",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093236.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093118.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035092.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035052.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035049.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676034986.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/VDzg5vQP5/1675836120.mp4",
# "https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200089.mp4",
# "https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200292.mp4",
# "https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200260.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173611.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173611.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675172752.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675172999.mp4"
# ]

# rows = ["",
#     "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035092.mp4",
#     "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035052.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035049.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676034986.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/VDzg5vQP5/1675836120.mp4",
#     "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530822.mp4",
#     "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530915.mp4",
#     "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530825.mp4",
#     "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530831.mp4"
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173379.mp4",
    # ]


# single aceFalse racket touched
# rows = ["",

# "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035205.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035245.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/da.stb6S8/1675752712.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/OMbWgFe4G/1675406694.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675172180.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173025.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173379.mp4",
# "https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200292.mp4",
# ""
# ]


# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093329.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093327.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093326.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093325.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093330.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093323.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093324.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093321.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093320.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093322.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093319.mp4"
# ]

# rows = ["","/home/multi-sy-008/videoverse/tennis_utils/match_9/match_9_1_17_34.mp4"]#,"https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kBd9m.FO4/1676988255.mp4","https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kBd9m.FO4/1676988155.mp4","https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kBd9m.FO4/1676988262.mp4","https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kBd9m.FO4/1676988298.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_13/match_13_00_05_33.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_9/match_9_1_03_23.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_12/match_12_0_27_32.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_10/match_10_00_47_30.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_6/match_6_1_42_51.mp4","/home/multi-sy-008/videoverse/tennis_utils/match_2/match_2_01_17_56.mp4","https://d1zxk9teuo4ijt.cloudfront.net/IUtwyjpTe/1676035092.mp4","https://d3my33k3mp21fy.cloudfront.net/footbal_test/Q2ElPa3lb/1669093236.mp4"]
# rows = ["","/home/multi-sy-008/videoverse/tennis_utils/match_2/match_2_2_35_40"]
# # rows = ["","/home/multi-sy-008/videoverse/tennis_utils/match_9/match_9_1_01_32.mp4","https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035245.mp4","https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/PJISwos4B/1676971529.mp4"]
# rows = ["",
# "https://d1zxk9teuo4ijt.cloudfront.net/KWyBBchfX/1676354959.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035051.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035051.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/4Uu6c4H5n/1675173379.mp4"]



# rows = ["",
# "https://d1zxk9teuo4ijt.cloudfront.net/15ytizwDs/1676355022.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/KWyBBchfX/1676354948.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530790.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/WLvfXzUYO/1676530857.mp4",
# "https://d1zxk9teuo4ijt.cloudfront.net/SLXN-600I/1676035068.mp4"
# ]

# rows = ["",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531610.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531694.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531696.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531650.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531645.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531610.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531612.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531609.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531563.mp4",
# # "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/hG3zQdey1/1678531564.mp4"]

# "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kCYdHxXjE/1677667324.mp4",
# "https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/kCYdHxXjE/1677667252.mp4"]
# rows = os.listdir("/home/multi-sy-008/videoverse/tennis_utils/match_1")
# rows = glob.glob("/home/multi-sy-008/videoverse/tennis_utils/match_1/*.mp4")
# rows = ["https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/0weHy0X4v/1678691853.mp4"]
print(rows[0])
for row in rows[:500]:
    try:
        # data = row.split(",")
        print(row)
        print(row.split(' '))
        link=row.split('\n')[0]
        ball_boxes = []
        frame_n = 0
        jsonResult_racket = {}
        jsonResult_ball = {}
        jsonResult_person = {}
        # print(sorted(glob.glob(folder + '*.*')))#, key=lambda x: int(x.split("/")[-1].split(".")[0])))
        # for file  in sorted(glob.glob(folder + '*.*'), key=lambda x: int(x.split("/")[-1].split(".")[0])):
        # for file in sorted(glob.glob(folder + '*.*'), key=lambda x: int(x.split("/")[-1].split(".")[0])):
        video = cv2.VideoCapture(link)
        saveFolder = link.split("/")[-1].split(".")[0]
        if os.path.exists(saveFolder) :print("ALERESDFSSD") 
        else: os.mkdir(saveFolder)
        while video.isOpened():
            frame_n+=1
            ret, frame = video.read()
            # h,w,_ = frame.shape
            # frame-=30
            # print(file)
            # frame = cv2.imread(os.path.join(folder,file))

            h,w,_ = frame.shape
            _, img_encoded = cv2.imencode('.jpg',frame)
            file = {'image': img_encoded.tobytes()}
            # openResponse = requests.post(url_ball,files= file)

            openResponse = requests.post(url_ball,files= file)

            if len(openResponse.json())>0:

                personList = []
                for result in openResponse.json():
                    # print(result)
                    xmin,ymin,xmax,ymax,conf,object_class = result["xmin"],result["ymin"],result["xmax"],result["ymax"],result["confidence"], result["name"]
                    ball_boxes.append([int(xmin),int(ymin)])
                    # print((int(xmin),int(xmax)),(int(xmin),int(xmax)))
                    cv2.rectangle(frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,0,255),2)
                    # cv2.putText(frame,str(conf),(int(xmin),int(ymin-10)),cv2.FONT_HERSHEY_SIMPLEX,.8,(0,0,255),1)
                jsonResult_ball.update({frame_n:openResponse.json()})

            # cv2.rectangle(frame,(int(w * 0.075),int(h * 0.075)),(w - int(w * 0.075),h - int(h * 0.075)),(255,255,0),3)
            cv2.imshow("img",frame)
            cv2.imwrite(f"{saveFolder}/{frame_n}.png",frame)
            cv2.waitKey(1)
        # cv2.destroyAllWindows()

            with open(f"{saveFolder}/{saveFolder}_ball.json", "w") as bouncecords:
                jsondata = json.dumps(jsonResult_ball,cls = NumpyEncoder)
                json.dump(jsondata,bouncecords)

    except Exception as e:
        print("ERRPRPRRPRPRPR", e)

        with open(f"{saveFolder}_ball.json", "w") as bouncecords:
            jsondata = json.dumps(jsonResult_ball,cls = NumpyEncoder)
            json.dump(jsondata,bouncecords)













#detections saved upto https://d3my33k3mp21fy.cloudfront.net/vendor/tennis/0weHy0X4v/1678691955.mp4