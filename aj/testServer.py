# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run a Flask REST API exposing one or more YOLOv5s models
"""

import argparse
import io

import torch
from flask import Flask, request
from PIL import Image

app = Flask(__name__)
models = {}

DETECTION_URL = "/v1/object-detection/<model>"



@app.route(DETECTION_URL, methods=["POST"])
def predict(model):
    if request.method != "POST":
        return

    if request.files.get("image"):
        # Method 1
        # with request.files["image"] as f:
        #     im = Image.open(io.BytesIO(f.read()))

        # Method 2
        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))

        print(f'Model {model}')

        if model in models:
            results = models[model](im, size=640)  # reduce size=320 for faster inference
            print(f'Results :: {results}')
            return results.pandas().xyxy[0].to_json(orient="records")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5002, type=int, help="port number")
    opt = parser.parse_args()
    all_models = ['yolov5s','yolov5s2','yolov5s3']
    models_path = ["yolov5/yolov5s.pt","sTyw2BYVM63VHl1.pt","mAxqoDB5zMZnd9m.pt"]
    
    for model_name, model_path in zip(all_models, models_path):
        models[model_name] = torch.hub.load('ultralytics/yolov5', 'custom', model_path)
        print(f'Model loaded ==> {model_name}')

    app.run(host="0.0.0.0", port=opt.port)


