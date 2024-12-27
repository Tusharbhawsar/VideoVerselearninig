# import pandas as pd
# import os
# import uuid
# df = pd.read_csv('/home/multi-lap-52/Downloads/Baseball/Home_run_clips_mar_1/Home_run.csv')
# for i in df:
#     urls=i["url"]
#     str_time=i["Str_time"]
#     end_time=i["End_time"]
#     name=uuid.uuid4() + ".mp4"
#     cmd=f"""ffmpeg -i {urls} -ss {str_time} -to {end_time} {name}"""
#     os.system(cmd)

# import torch
# '''import utils'''

# # Check if CUDA (GPU support) is available
# if torch.cuda.is_available():
#     # Configure PyTorch to use GPU
#     device = torch.device("cuda")
#     print("Using GPU for computation.")
# else:
#     # If CUDA is not available, use CPU
#     device = torch.device("cpu")
#     print("CUDA is not available. Using CPU for computation.")

# import pandas as pd
# import os
# import uuid

# df = pd.read_csv('/home/link-lap-24/Downloads/replay_extend/rr_vs_sun.csv')
# print(df)
# urls = df["url"]
# print(urls)
# for index, row in df.iterrows():
#     urls = row["url"]

#     str_time = row["-10"]
#     end_time = row["10+"]
#     print(str_time,end_time)
#     # name = str(uuid.uuid4()) + ".mp4"
#     name=str(index) + ".mp4"
#     # cmd = f"ffmpeg -ss {str_time} -to {end_time} -i {urls} {name}"
#     cmd = f"ffmpeg -ss {str_time} -to {end_time} -i {urls} -c copy {name}"

#     os.system(cmd)


# import json
# import os

# with open("/home/link-lap-24/Downloads/netball_event/Netball.json") as file:
#     data=json.load(file)
#     print(data)
#     mat_1=data[1]
#     url=data[1]["sourceUrl"]
#     # print(url)

#     for name,i in enumerate(mat_1["event"]):
#         st=i["startTime"]
#         end=i["endTime"]

#         cmd=f"ffmpeg -ss {st} -to {end} -i {url} {name}.mp4"
#         os.system(cmd)

##for save the video in specfic folder
import json
import os

# Ensure the output directories exist
os.makedirs('events', exist_ok=True)
os.makedirs('non_events', exist_ok=True)

with open("/home/link-lap-24/Downloads/netball_event/netball.json") as file:
    data = json.load(file)
    
    # Fetch the first match
    mat_1 = data[0]
    url = mat_1["sourceUrl"]
    
    for name, i in enumerate(mat_1["event"]):
        st = i["startTime"]
        end = i["endTime"]
        
        # Determine whether the event is an "event" or "non-event"
        event_type = i.get("event", "non_event")
        if event_type == "event":
            folder = 'events'
        else:
            folder = 'non_events'

        # Create the output file path with proper naming
        output_file = os.path.join(folder, f"{name}.mp4")
        
        # ffmpeg command to trim the video
        cmd = f"ffmpeg -ss {st} -to {end} -i {url} {output_file}"
        os.system(cmd)


# import json
# import os
# import glob

# video_path="/home/link-lap-24/Downloads/clips/fin_replay/im/en/"
# comp_path=glob.glob(video_path + "*.mp4")

# for name,i in enumerate(comp_path):
#     # print(i)
#     st="00:00:01"

#     cmd=f"ffmpeg -ss {st} -i {i} {name}_.mp4"
#     os.system(cmd)


# import pandas as pd
# import os
# from tqdm import tqdm
# df = pd.read_csv('Home_run.csv')
# def crop_video(video_path, start_time, duration, output_path):
#     cmd = f'ffmpeg -v error -ss {float(start_time)} -i {video_path} -t {float(duration)} {output_path}'
#     os.system(cmd)
# with tqdm(total=len(df), desc="Progress") as pbar:
#     for video_url, start_time, end_time in zip(df['url'], df['Str_time'], df['End_time']):
#         if not os.path.exists('cropped_videos'):
#             os.makedirs('cropped_videos')
#         output_name = video_url.split('/')[-1]
# #         output_name=df["Tags"]
# #         output_name =str(name)
#         output_path = f"cropped_videos/{output_name}"

# import os
# import json
# import subprocess

# # Load the JSON data
# with open('/home/multi-lap-52/Downloads/Baseball/new/Baseball-Replay-Clips-Time-Stamp-Tagging-05-06-2024-14-24-47.json', 'r') as file:
#     data = json.load(file)

# # Function to download and save clips
# def download_clip(source_url, start_time, end_time, output_path):
#     duration = end_time - start_time
#     # Using ffmpeg to download the clip
#     command = [
#         'ffmpeg', 
#         '-ss', str(start_time), 
#         '-i', source_url, 
#         '-t', str(duration), 
#         '-c', 'copy', 
#         output_path
#     ]
#     subprocess.run(command, check=True)

# # Create the folder structure and download clips
# for item in data:
#     id_folder = os.path.join('clips', item['_id'])
#     os.makedirs(id_folder, exist_ok=True)
    
#     for event in item['event']:
#         event_folder = os.path.join(id_folder, event['event'])
#         os.makedirs(event_folder, exist_ok=True)
        
#         clip_filename = f"{event['startTime']}-{event['endTime']}.mp4"
#         clip_path = os.path.join(event_folder, clip_filename)
        
#         download_clip(item['sourceUrl'], event['startTime'], event['endTime'], clip_path)
#         print(f"Downloaded clip: {clip_path}")

# print("All clips downloaded and organized.")

# import os
# import json
# import subprocess

# # Load the JSON data
# with open('/home/multi-lap-52/Downloads/Baseball/new/Baseball-Replay-Clips-Time-Stamp-Tagging-05-06-2024-14-24-47.json', 'r') as file:
#     data = json.load(file)
# video_path="/home/link-lap-24/Downloads/clips/fin_replay/im/st/"

# # Function to download and save clips
# def download_clip(source_url, start_time, end_time, output_path):
#     # Adjusting start and end times
#     adjusted_start_time = start_time + 1
#     adjusted_end_time = end_time 
#     duration = adjusted_end_time - adjusted_start_time
    
#     # Using ffmpeg with GPU acceleration to download the clip
#     command = [
#         'ffmpeg', 
#         '-hwaccel', 'cuda',  # Enable GPU acceleration
#         '-ss', str(adjusted_start_time), 
#         '-i', source_url, 
#         '-t', str(duration), 
#         '-c:v', 'h264_nvenc',  # Use NVIDIA encoder
#         '-c:a', 'copy',  # Copy the audio stream
#         output_path
#     ]
#     subprocess.run(command, check=True)

# # Create the folder structure and download clips
# for item in data:
#     id_folder = os.path.join('clips', item['_id'])
#     os.makedirs(id_folder, exist_ok=True)
    
#     for event in item['event']:
#         event_folder = os.path.join(id_folder, event['event'])
#         os.makedirs(event_folder, exist_ok=True)
        
#         clip_filename = f"{event['startTime']+1}-{event['endTime']-1}.mp4"
#         clip_path = os.path.join(event_folder, clip_filename)
        
#         download_clip(item['sourceUrl'], event['startTime'], event['endTime'], clip_path)
#         print(f"Downloaded clip: {clip_path}")

# print("All clips downloaded and organized.")
#         duration = float(end_time) - float(start_time)
#         crop_video(video_url, start_time, duration, output_path)
#         pbar.update(1)
