import cv2
import json
import numpy as np
import subprocess as sp
import os

video_path = "/home/link-lap-24/ayush/1696917788.mp4"
prefix = "IntvsPenBCLA23"

# get video config
command = ['ffprobe',
           '-v', 'error',
           '-select_streams', 'v:0',
           '-show_entries', 'stream=width,height,duration',
           '-of', 'json', video_path]
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**5)
video_info = json.loads(pipe.stdout.read())
width = video_info['streams'][0]['width']
height = video_info['streams'][0]['height']
duration = float(video_info['streams'][0]['duration'])
pipe.stdout.flush()

# Create folders for each key
output_folders = {'g': 'ground', 'p': 'pitch', 'f': 'focus_player', 'a': 'audience','o': 'other'}
for folder in output_folders.values():
    os.makedirs(folder, exist_ok=True)

# Extract required frames from video to buffer
command = ['ffmpeg',
           '-loglevel', 'quiet',
           '-i', video_path,
           '-vf', 'fps=1',
           '-qscale:v', '1',
           '-qmin', '1',
           '-f', 'image2pipe',
           '-pix_fmt', 'rgb24',
           '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

# read frames from buffer
idx = 0
try:
    while True:
        raw_image = pipe.stdout.read(width * height * 3)
        if not raw_image:
            break
        frame = np.frombuffer(raw_image, dtype='uint8')
        frame = frame.reshape((height, width, 3))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('current frame', frame)
        k = cv2.waitKey(0) & 0xff
        # press 'Esc' key to stop processing
        if k in [ord(key) for key in output_folders]:
            idx += 1
            key_pressed = next(key for key, value in output_folders.items() if ord(key) == k)
            folder_name = output_folders[key_pressed]
            file_path = os.path.join(folder_name, f"{prefix}_{idx}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"Frame saved to {file_path}")
        if k == 27 or k == ord('q'):
            break
finally:
    pipe.stdout.flush()

