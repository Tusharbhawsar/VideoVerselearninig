import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from ultralytics import YOLO
import numpy as np
import argparse
from flask import Flask, request, jsonify
import sys

class Toch(Flask):
    def __init__(self, host, name, model):
        super(Toch, self).__init__(name, static_url_path='')
        self.host = host
        self.define_uri()
        self.requests = {}
        self.model = model

    def define_uri(self):
        self.provide_automatic_option = False
        self.add_url_rule('/afl_ball_detection', None, self.start, methods=['POST'])

    def prediction_api_new(self, image_path):
        rect_player = []
        try:
            results = self.model.predict(source=image_path,conf=0.05,imgsz=1024)
            results = results[0]
            result_box = results.obb.xyxy.cpu().numpy()        
            labels = results.obb.cls.tolist()  
            scores = np.array(results.obb.conf.tolist(), dtype="float").round(2)           
            rect_player = []       
            for rect,lable,score in zip(result_box.tolist(),labels,scores):
                lable = int(lable)
                if lable == 0:
                    rect = list(int(x) for x in rect)
                    rect_player.append({'coordinates':rect,'label':"ball",'score':score})
            return rect_player
        except:
            return rect_player

    def start(self):
        print(("json:", request.get_json()))
        if request.method == 'POST':
            body = request.get_json()
            image_path = body['image_path']
            data_send = self.prediction_api_new(image_path)
            res = dict()
            res['status'] = '200'
            res['result'] = data_send
            return jsonify(res)

def importargs():
    parser = argparse.ArgumentParser('This is a server')
    parser.add_argument("--host", "-H", help="host name running server", type=str, required=False, default='localhost')
    parser.add_argument("--port", "-P", help="port of running server", type=int, required=False, default=3007)
    args = parser.parse_args()
    return args.host, args.port

def main():
    host, port = importargs()
    model = YOLO('yolov8m-obb.pt')
    server = Toch(host, 'YOLOV8_Model_Server', model)
    server.run(host=host, port=port)

if __name__ == "__main__":
    main()