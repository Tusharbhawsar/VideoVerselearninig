
matchListFile = "/home/link-lap-24/jupyter_files/new/api/Magnifi.csv"
import pandas as pd
# import requests

# # matchList = open(matchListFile,"r")
df = pd.read_csv(matchListFile)

import requests



for data in df.itertuples():
    # print(data.matchstreamId)
    streamIdMetaDataLink = "https://dbapi.magnifi.ai/get/clips/"+f"{data.matchstreamId}"+"?limit=1000&pageNo=1&filters={%22players%22:[],%22events%22:[],%22sortBy%22:%22TIME_DESCENDANT%22,%22aspectRatio%22:%22%22,%22playBackSpeed%22:[],%22webhookPublish%22:%22%22,%22clipData%22:{}}&daterange=[]&sort={%22start_time%22:-1,%22_id%22:1}&type=all&search=&aspectRatio=&webhookPublish=&isManualUpload=false&skipCount="
    url = streamIdMetaDataLink
    # print(url)
    response = requests.request("GET", url)
    # print(response.json())
    # jsonss = json.load(linkSall)
    jsonss = response.json()
    print(jsonss.keys())
    clips = jsonss["clips"]
#     print(clips)
    with open(f"{data.matchName}.csv","w") as linksFile:
        print(data.matchName)
        for clip in clips:

            linksFile.write(f"{clip['videoUrl']}\n")
