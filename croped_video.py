import os
import shutil
import uuid

#w= 1920
#h = 1080

#crop=w:h:x:y"

#(130,237)
#(886,1080)

import glob

images_folder = "/home/link-lap-24/tushar_data/images/smoking/"

cropped_folder = "/home/link-lap-24/tushar_data/images/smoking_result/"

data = glob.glob(images_folder+'*.*')

for i in data:
	print("==============================", i)
	cmd = 'ffmpeg -i {}%d.jpg -vf "crop=450:800:660:886" {}%d.jpg'.format(images_folder, cropped_folder)
	os.system(cmd)




#ffmpeg -i http://164.52.211.24:3001/test/l3aKk__Vs_video.mkv -vf "crop=w:h:x:y" /content/frames/%d.jpg

#match1 = (99,998) x1,y1  x=99, y=998
#(1808,1053) x2,y2

#height = 1055 - 994 #998      (107,994)(1815,1055)

#width = 1815 -107 #99



#ffmpeg -i "/home/rajput/Desktop/1new.jpg" -vf "crop=1708:61:107:994" %d.jpg