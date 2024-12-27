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

strem_mul = [
    "B6IaRxN9Z", "rN0HAxlW0", "JCqnook4X", "vhvIsfKFg", "lYxtsvqAN", "z2Soyt9Q1", 
    "2ekvRbrwP", "Tk-0UrPMd", "uUzRzlXxa", "eswCfHw-s", "3GHlowC6d", "bJLh9NV.h", 
    "g9-ce4LaV", "wpxtors-c", "nNy-RcUn-", "nBcYgklpr", "e9mVFd6Au", "Y0u.B9HfR", 
    "jO7gYB-k0", "SlirngQQE", "QCg7l9Q5P", "dOkObX9Oc", "iOYGOZ-WV", "sdBpCCCMw", 
    "nreLiIGUc", "rkA.vJShM", "bWKqmPWrz", 
    "XRtcsFdMj", "tdUPTMCiW", "ze5a8nvcI", "q7UVRHDC6", "igWHfOSpG", "ULZPdOCy0", 
    "fY5DNv5Fw", "HIJq99sld", "ifDNIoBC", "uexc62wzL", "-oHSABtj9", "nTEnBgTaa", 
    "Fb9YN7YWt", "DJBopXBBk", "iis0McVbL", "q1wxxkKi7", "pznloKC8n", "oQtnmvYmD", 
    ".eLInPfMI", "i2fIX5syL", "9ER8IC9oA", "7J9CokpwZ", "0-NytCIXv", "7rbt9cyno", 
    "Bf5pl66LE", "5VVU5XaAI", "R4D2rU1ID", "Ic3jGW6wm", "LGDMRLepZ", "VeUWHb2iI", 
    "gG2ANssJ8", "ePJSAutfB", "LaiNMINpw", "C4srmCjCC", "n2CYoy48t", "Fbl8JC0Wp", 
    "xpFNSjM0A", "ZufV8LWhM", "oOC.aK1yg", "QVQO.mJJO", "ZCDboOesB", "bNmspFO8j"
]
events = ["WKT", "Wicket!", "Wicket", "Run Out", "Runout", "stumping", "Stumping", "Stump", "stump"]
all_data = []
for count, i in enumerate(strem_mul, start=1):
    print(i)
    streamIdMetaDataLink = f"https://api.magnifi.ai/get/clips/{i}?limit=1000&pageNo=1&filters={{\"players\":[],\"events\":[],\"sortBy\":\"TIME_DESCENDANT\",\"aspectRatio\":\"\",\"playBackSpeed\":[],\"webhookPublish\":\"\",\"clipData\":{{}}}}&daterange=[]&sort={{\"start_time\":-1,\"_id\":1}}&type=all&search=&aspectRatio=&webhookPublish=&isManualUpload=false&skipCount="
    response = requests.get(streamIdMetaDataLink)
    jsonss = response.json()
    clips = jsonss.get("clips", [])
    data = []
    for clip in clips:
        start_time = clip.get('start_time')
        end_time = clip.get('end_time')
        video_url = clip.get('videoUrl')
        clip_data = clip.get('clipData', {})
        if clip_data is None:
            clip_data = {}
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
csv_file_path = "viacom.csv"
df.to_csv(csv_file_path, mode='w', header=True, index=False)
print("All data appended to CSV file successfully.")
