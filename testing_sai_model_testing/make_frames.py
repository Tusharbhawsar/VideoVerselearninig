import time
import subprocess as sp
import os
import glob

def make_frames_from_video(input_video, fps, output_folder):
    st = time.time()
    cmd = f"ffmpeg -i {input_video} -qscale:v 0 -vf fps={fps} {output_folder}%d.jpg"
    ps = sp.Popen(cmd.split())
    ps.wait()
    et = time.time()
    print(f'Total time taken by frame is {et - st}')
    return [os.path.abspath(i) for i in sorted(glob.glob(output_folder + '*.jpg'), key=lambda x: int(x.split("/")[-1].split(".")[0]))]