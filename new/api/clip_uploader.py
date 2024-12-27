import csv
import requests
import json

url = "https://api.magnifi.ai/sony_clips/create"

with open('football.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        video_url = row['video_url']
        stream_id = row['stream_id']
        sport = row['sport']
        
        ai_scene_id = video_url.split('/')[-1][-9:-4]
        

        payload = {
            "config_data": {
                "sport": "football",
                "scene_no": "1730805938_5592365",
                "start_time": 0,
                "end_time": 15,
                "machine_output": "",
                "clipData": {},
                "timestamp": 1730805938,
                "label": "shortclips",
                "duration": 15,
                "fileSize": 0,
                "streamId": "bzoxUsX1N",
                "url": video_url,
                "thumbnailUrl": "",
                "thumbnails": [],
                "vertical_video": ""
            },
            "aiSceneId": ai_scene_id
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        

        print(f"Response for {video_url}: {response.status_code}, {response.text}")
