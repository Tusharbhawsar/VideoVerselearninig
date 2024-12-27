import imagehash
import os
import glob
from PIL import Image

def frame_extract(video_folder,duration=5):
    read_videos=glob.glob(os.path.join(video_folder + "*.mp4"))
    for video in read_videos:
        folder_name=os.path.splitext(os.path.basename(video))[0]
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        print(f"Extracting frame from {video} to {folder_name} folder.")
        cmd=f"ffmpeg -t {duration} -i {video} -q v 1 {folder_name}/%d.jpg"
        os.system(cmd)

#extractn the frames in a specific folder

def imag_hash(img_folder):
    hash_values=[]
    path=glob.glob(os.path.join(img_folder + "*.jpg"))
    for img in path:
        values=imagehash.average_hash(Image.open(img),hash_size=16)
        hash_values.append(values)

    return hash_values
#generating hash values of a given images a save into list

def find_duplicated_videos(video_folder,duration=5):
    frame_extract(video_folder,duration)
    video_hashes={}

    for video in glob.glob(os.path.join(video_folder, "*.mp4")):
        folder_name=os.path.splitext(os.path.basename(video))[0]
        img_folder=os.path.join(video_folder,folder_name)
        hashes=imag_hash(img_folder)

        video_hashes[video]=hashes

    duplicates={}

    videos=list(video_hashes.keys())
    for i in range(len(videos)):
        for j in range(i + 1,len(videos)):
            












video_path = "/home/link-lap-24/jupyter_files/duplicate_vide_golf_june7/videos/"
