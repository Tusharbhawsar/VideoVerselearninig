import make_frames
import cv2, pickle
from fastai.imports import *
from fastai.vision import *
from fastbook import *
import torch, timm 

video_list = ["https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440585.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440589.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440546.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440540.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440530.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440486.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440485.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440435.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440379.mp4",
"https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440381.mp4"]

for video_url in video_list:
    # video_url = 'https://d1zxk9teuo4ijt.cloudfront.net/bK0s7wsih/Crwn2HmhQ/Clips/AI_Clips/Crwn2HmhQ/1685440589.mp4'
    num =video_url.split('.mp4')[0].split('/')[-1]
    out_fol = f'./{num}/'
    if not os.path.exists(out_fol): os.mkdir(out_fol)
    fps = 15
    frames = make_frames.make_frames_from_video(video_url, fps=fps, output_folder=out_fol)
    # print('frames ::',frames)
    try:
        for i_path in frames:
            frame = cv2.imread(i_path)
            path = i_path.split('.')[0]
        #     print(path)
            model = load_learner('nBbe3vLCdzmFRE7.pkl',cpu=True)
            # model = pickle.load(open('model.pkl', 'rb'))
            pred = model.predict(i_path)
            cat = ['dead_filter','non_dead_filter']
            result = {}
            for i, j in enumerate(pred[2]):
        #         print(i,j)
                result[cat[i]] = round(float(pred[2][i])*100, 3)
                text = "Activity: {} ".format(result)
        #         print("this is the final results",text)
                cv2.putText(frame, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,1.25, (0, 255, 0), 3)
                cv2.imwrite(path+".jpg",frame)
    except:
        print(f'missed for {num}')
