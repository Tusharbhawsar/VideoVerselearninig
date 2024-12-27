import json

matchListFile = "/home/link-lap-24/collectClips/Magnifi.csv"
import pandas as pd
import requests

# matchList = open(matchListFile,"r")
df = pd.read_csv(matchListFile)
streamIdMetaDataLink = "https://km.magnifi.ai/api/v1/sony_clips/get/"
for data in df.itertuples():
    print(data.matchstreamId)
    url = streamIdMetaDataLink+str(data.matchstreamId)
    print(url)
    response = requests.request("GET", url)
    print(response.json())
    # jsonss = json.load(linkSall)
    jsonss = response.json()
    print(jsonss.keys())
    clips = jsonss["clips"]
    # print(clips)
    with open(f"{data.matchName}.txt","a") as linksFile:
        
        for clip in clips:
            # if "ace_serve" in clip["filter"]:
            # if "Serve Point" in clip["filter"] or "Set Point" in clip["filter"] or "game Point" in clip["filter"]:
                # if 5<clip["duration"]<10:
            linksFile.write(f"{clip['videoUrl']}\n")
            command = f"wget {clip['videoUrl']}"
            import os
            os.system(command)


# print("Serve Point" in passList)
