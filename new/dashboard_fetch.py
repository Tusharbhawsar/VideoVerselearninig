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

strem_mul = ["JqmwEQPY8","p7Vi07FHO","3erZmdMHU","zLGbj40oP","F1DpL-zer","NyFJA3hF6","FiJskkDJb","UTtyMGP0V","q1s6XvSBf","2CQKOAqMg","q516v.BGn","FLcSbOtiY","byylsKApP","vkeH8vLfd","jr9gyXZAM","rOJ71hckC","UW.0ZYld3","XJufSxBii","M4Vg1b7cW","UkITNuTyE","LuaD15KCu","jzbWG7VCR","ILZUy0fd5","7wQGa2i4V","BS5fqytxN","Gd-qVHFSZ","vsP0UkY0n","Rtz-aNAel","kXWf6wCeE","d8HSWYDMG","b2SSBlXtc","KmxGmUcBj","75JtBJmvv","42aKDnarv","M3Z.kltkZ","YsRvHUmGI","euNfOFWxM","SjVCgWZ3R","5RUmGcPJu","MBlvbNt5w","MmHvoJWja","AwLtcxugL","IFC0m8j9-","f7VRPO7.h","7W5HWVeJb","cbKN0Sq5f","qVyfl3HEz","5V2Hk2qbz","stm.pSPP7","xjwtdlDKh","YRzwPKnw0","NNc5LdzRO","kojGMivXu","Rg0QzdVrZ","FIOiJukig","V0WSE-go4","3vawbpZK2","pMmM9PGJE","nGzJLu8Ou","4hUYeNc5z","Z2TmskTtZ","T7YdPx4ve","uo9UT9jMJ","Hoc3RlQRz","-IWp6I0cc","fWdZUTRnF","YroQTpqQN","DXw8LyeZ4","XZleUWezn","RfsUQRC4.","j-EBV9PPc","bM6TN1XoS","dKc-y9xLG","OyoMl5XCB","zJ8MyDmQN","TtxIAfmOC","wUR20mDgG","PLJgQd1AE","wQfhozMua","fp8m2z0vw","JQAIuA7qz","8AumwZRff","CMaBkxzEA","eT9MbWoC0","NSnKUWXVL","RDU1qmkTx","SIk4BaiB.","bTNz62YTR","4-ExlwEhA","aIxeKdorA","a0k9a7pA2","Qwp.BhKSC","EsX99g8yW","bZn1ir1Yb","6NA940TUr","QFkgpVrml","eUlMKnBjK","llbqpyTRo",".-BG77wy9","R-8YpeEVm","4ketQNJZ9","1e90rHnV.","Negqiw.9a","hOT.0EBgv","MfqGVq0Xf","-ZqhFBuer","oWC6yKt1u","2hbCgYcRA","NWSL2lWnm","wOytIZwFq","HqnGV03Wu","PH0D5EOyc","9LtEs7yGi","DN6mc3Q8x","-46Jgg0Nt","VQit80AZ.","GddYiRknb","CO2nwDaC4","EspTPubbr","gdumHBfNH","-ITTcVMla","-fqQo1NjT","IRm5koL07","CT0xt10kY","1HSkj5lLA","IfuprJKJi","hC7x1uLW-","XPlCvSOXz","VQqKp6hRP","GncGGHump","4BmdeR066","WoIjdY0E-","cpYFKClkx","IVK0ziCQs","rpJrVPigs","Squ9A3HDZ","07OPolngo","O3LB0DTXL","BmWd7TwXq","noANOsNvU","kmzuo6N.W","aRGoOi9yP","olLwYiyXQ","t7t2D2wXO","5FDy6HfrL","f8XjMVht-","joO2YH1M4","PHZjVLgiX","TiqKTkIne","uxewWQc20","VX57M3jnW","rzcZKa8eT","zvyK.TFVb","gup.2D3sG","gzz-CRIuu","auf87CENm","HBHrEGpnn","dS45nQyCY","8-kEQOtBc","3PjWl3Cca","zeI5B1mtA","iuwshOK5U","wGQYKIoXr","DbXpWu9-O","ny5i8SqSw","yZRi90PYZ","ozp0o7h49","UGTdnreM6","DBmITv-uY","QsPfjeToP","FrK6iV.OP","4AFl.h9Ry","s79pmxgiS","2VdtmBX8A","v23q3dACH","Puk28PL0i","V23OGqamB","41REyHJX2V","IwxAWC7Q7","Hhey1NOx1","5s2ikzyzA","Q6k8EXn1J","ZlxDrwGP9","Q1IgVmLfb","nyL7LItDT","IjzI7ig.a","C0NeO2J-h","bRiHfYYHG",".GQJgIrFY","2DdbIDVAn","x6MY587qb","oJ-w4u7HL","x9Nbf2eLV","T-dTUFtlF","TxFbIKLqh","vUrwitImc","jmWJv5LQv","aXCqD.K47","hi0izmpyk","Ts6.VkN-D","nt7PuJMe8",".fL1GbA1W","NrpzwTnyd","6SF8wcDC2","GBOZXDzWo","GHSV7MwWl",".g2vtMPFT","VOoUIql66","HyQXwzeK8","QMM1KT.Vl","XWIus-KlI","Pw1amsM39","eUdE.YB1B","cRAJK-zxK","yoKgYvHC2","pCYuuQVH6","0rrtojq1x","6tDw.jzAD","DxkSd-o2.","3pWgbfKJN","QutBxmbMz","o1dwFqdec","1t362T1Al","84JO11oxM","pcUlgWWJT","emYDaN7Yt","MrZC2Dn9w","oizGPnzzw","U4WXL6YLl","YGUo.wBYe","uPEDKczjz","0OaIeflyw","rB-Rq9JVg","v4A-eZ5WZ","N1-9eQ1B-","WibAuLgOB","H3wmR2KKf","KzkjCT0bl","5vBnEaKU7","CdFW-TaCu","UMGV.509b","J.UszoKe1","uD9A0HpsI","1PPSELUH-","ZoY-c7RzP","fQDfIv9q9","jlrdQzL8U","B3mL9bqP4","g9W9Ana6g","kCpf2ng-8","uRNFVYNuz","J5Gnz3DIJ","EJIBVyO9d","fEOO3FyRi","Rh.5RC3Rb","EtvAUhXYT","O9jZ8J-K8","z077lmVuu","oNODQub7S","zEgpZPgRm","vfRooOJpa","D6VA.Iiia","G.QSUH2wy","DursMHlNF","gHkq2GayI","9OzlQykBi","M.jPXUgwG","E0nPMLmvX","RDZGV.A47","RhgExEbS.","Fg-YUKCtt","jKS3ZCx2y","EpYRDECBz","9TTNMXfhG","rZBiBokIQ","rvcMPsWox","Mt42HPV1T","uccCxg3rN","8y86luz1B","aaThaXYRf","Ccx1r5qwc","MwSW9VBie","AUjjTmUKE","f-WXKofWA","3neJ0f.Bg","ellbdqyfm","zhbvMOrUP","EK6Qs3cyp","OA43pewjD","kL6X7vdVM","O7.Rayp2Z","XkIPfoVQJ","m2.H4CjBV","FJGyH2IKV","J3XSWSp2y","oKSBPj.cC","keLbepoYM","kNLorl33n","Wa5N4psPv","hMNE6Guzk"]
events = ["Chance Replay","Chance_Replay","Chance","Corner Kick","Foul","Foul Replay","Foul_Replay","Goal","Goal Replay.","Goal_Replay.","Goal Replay","Goal_Replay","Save","Save Replay","Goal_replay","chance replay","chance","corner kick","foul","foul replay","goal","goal replay.","goal replay","save","save replay","goal_replay"]
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