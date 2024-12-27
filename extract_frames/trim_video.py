import cv2
import json
import numpy as np
import subprocess as sp

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

# Extract required frames from video to buffer
command = ['ffmpeg',
           '-loglevel', 'quiet',
           '-i', video_path,
           '-vf', 'fps=30',
           '-qscale:v', '1',
           '-qmin', '1',
           '-f', 'image2pipe',
           '-pix_fmt', 'rgb24',
           '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

# Initialize variables for trimming
trimming = False
trimmed_frames = []

try:
    while True:
        raw_image = pipe.stdout.read(width * height * 3)
        if not raw_image:
            break
        frame = np.frombuffer(raw_image, dtype='uint8')
        frame = frame.reshape((height, width, 3))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if trimming:
            trimmed_frames.append(frame)

        cv2.imshow('current frame', frame)
        k = cv2.waitKey(1) & 0xff

        # press 's' key to start trimming
        if k == ord('s'):
            trimming = True
            trimmed_frames = []

        # press 'e' key to end trimming
        elif k == ord('e'):
            trimming = False
            for idx, trimmed_frame in enumerate(trimmed_frames):
                cv2.imwrite(f"{prefix}_trimmed_{idx}.jpg", trimmed_frame)

        # press 'Esc' key to stop processing
        elif k == 27 or k == ord('q'):
            break
finally:
    pipe.stdout.flush()
    cv2.destroyAllWindows()

# Save trimmed video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_trimmed.mp4', fourcc, 1, (width, height))

for frame in trimmed_frames:
    out.write(frame)

out.release()

