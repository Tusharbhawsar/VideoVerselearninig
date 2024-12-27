import imagehash
from PIL import Image
import glob
import os
import csv

def frames_extract(video_folder, duration=5):
    read_videos = glob.glob(os.path.join(video_folder, "*.mp4"))
    for video in read_videos:
        folder_name = os.path.splitext(os.path.basename(video))[0]
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        print(f"Extracting frames from {video} to {folder_name} folder.")
        # Extract frames only from the first 'duration' seconds
        cmd = f"ffmpeg -t {duration} -i {video} -q:v 1 {folder_name}/%d.jpg"
        os.system(cmd)

def imag_hash(img_folder):
    hash_values = []
    path = glob.glob(os.path.join(img_folder, "*.jpg"))
    for img in path:
        values = imagehash.average_hash(Image.open(img), hash_size=16)
        hash_values.append(str(values))
    return hash_values

def find_duplicate_videos(video_folder, duration=5):
    frames_extract(video_folder, duration)
    video_hashes = {}
    
    for video in glob.glob(os.path.join(video_folder, "*.mp4")):
        folder_name = os.path.splitext(os.path.basename(video))[0]
        img_folder = os.path.join(video_folder, folder_name)
        hashes = imag_hash(img_folder)
        
        video_hashes[video] = hashes
    
    duplicates = {}
    videos = list(video_hashes.keys())
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            if any(hash in video_hashes[videos[j]] for hash in video_hashes[videos[i]]):
                if videos[i] not in duplicates:
                    duplicates[videos[i]] = []
                duplicates[videos[i]].append(videos[j])
    
    return duplicates

video_path = "/home/link-lap-24/jupyter_files/duplicate_vide_golf_june7/videos/"
duplicates = find_duplicate_videos(video_path)
print("Duplicate videos found:")
with open("duplicate.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Video", "Duplicates"])

    for video, dupes in duplicates.items():
        writer.writerow([video, ",".join(dupes)])
        print(f"{video} has duplicates: {dupes}")
