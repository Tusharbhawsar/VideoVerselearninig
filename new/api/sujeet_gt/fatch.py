import requests
import json
import pandas as pd

def convert_seconds_to_time(total_seconds):
    print("total_seconds",total_seconds)
    try:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, int(seconds))
    except:
        return None
    

i_value = "LJJsR8UOO"
url = f"https://api.magnifi.ai/get/clips/{i_value}?limit=1000&pageNo=1&filters={{\"players\":[],\"events\":[],\"sortBy\":\"TIME_DESCENDANT\",\"aspectRatio\":\"\",\"playBackSpeed\":[],\"webhookPublish\":\"\",\"clipData\":{{}}}}&daterange=[]&sort={{\"start_time\":-1,\"_id\":1}}&type=all&search=&aspectRatio=&webhookPublish=&isManualUpload=false&skipCount="
response = requests.get(url)

result=[]
if response.status_code == 200:
    data = response.json()
     
    for clip in data['clips']:
        input_url=clip.get("videoUrl")
        start_time=clip.get("start_time")
        endtime=clip.get("end_time")
        clip_data = clip.get("clipData", {})
        outcome = clip_data.get("outcome",None)
        # print(outcome)

        con_st = convert_seconds_to_time(start_time)
        con_end = convert_seconds_to_time(endtime)

        result.append({
            "urls":input_url,
            "start_time":con_st,
            "end_time":con_end,
            "event":outcome
        })

data = pd.DataFrame(result)
data_reversed = data.iloc[::-1]
# df_reversed = df.iloc[::-1]

data_reversed.to_csv("match1.csv",index=False)