import pandas as pd
import requests
from datetime import datetime

def convert_seconds_to_time(total_seconds):
    print("total_seconds",total_seconds)
    try:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, int(seconds))
    except:
        return None

strem_mul = ["iEVvejwdQ"]
events = []
all_data = []
for count, i in enumerate(strem_mul, start=1):
    streamIdMetaDataLink = f"https://dbai.magnifi.ai/get/clips/{i}?limit=1000&pageNo=1&filters={{\"players\":[],\"events\":[],\"sortBy\":\"TIME_DESCENDANT\",\"aspectRatio\":\"\",\"playBackSpeed\":[],\"webhookPublish\":\"\",\"clipData\":{{}}}}&daterange=[]&sort={{\"start_time\":-1,\"_id\":1}}&type=all&search=&aspectRatio=&webhookPublish=&isManualUpload=false&skipCount="
    response = requests.get(streamIdMetaDataLink)
    jsonss = response.json()
    clips = jsonss.get("clips", [])
    data = []
    for clip in clips:
        start_time = clip.get('start_time')
        end_time = clip.get('end_time')
        video_url = clip.get('videoUrl')
        clip_data = clip.get('clipData', {})
        outcome = clip_data.get('outcome', None)
        if outcome in events:
            start_time = convert_seconds_to_time(start_time)
            end_time = convert_seconds_to_time(end_time)
            print("this is the time come by the stream",start_time,end_time)
            data.append([start_time, end_time, video_url, outcome, i])
    if data:
        all_data.extend(data)
        all_data.append([None, None, None, None, None])

df = pd.DataFrame(all_data, columns=['start_time', 'end_time', 'video_url', 'outcome', 'stream_id'])
csv_file_path = "replay_all_clips_data_ne.csv"
df.to_csv(csv_file_path, mode='w', header=True, index=False)
print("All data appended to CSV file successfully.")
