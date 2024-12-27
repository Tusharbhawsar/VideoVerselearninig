import imagehash
from PIL import Image
import glob
import os
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor

def frames_extract(video_url, folder_name, duration=5):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    print(f"Extracting frames from {video_url} to {folder_name} folder.")
    # Extract frames only from the first 'duration' seconds
    cmd = f"ffmpeg -t {duration} -i \"{video_url}\" -q:v 1 {folder_name}/%d.jpg"
    subprocess.run(cmd, shell=True, check=True)

def imag_hash(img_folder):
    hash_values = []
    path = glob.glob(os.path.join(img_folder, "*.jpg"))
    for img in path:
        values = imagehash.average_hash(Image.open(img), hash_size=16)
        hash_values.append(str(values))
    return hash_values

def process_video(url, duration):
    folder_name = os.path.splitext(os.path.basename(url))[0]
    frames_extract(url, folder_name, duration)
    hashes = imag_hash(folder_name)
    # Clean up the extracted frames
    for img_file in glob.glob(os.path.join(folder_name, "*.jpg")):
        os.remove(img_file)
    os.rmdir(folder_name)  # Remove the folder
    return url, hashes

def find_duplicate_videos(video_urls_file, duration=5):
    video_hashes = {}

    with open(video_urls_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        video_urls = [row[0] for row in reader]

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_video, url, duration) for url in video_urls]
        for future in futures:
            url, hashes = future.result()
            video_hashes[url] = hashes

    duplicates = {}
    videos = list(video_hashes.keys())
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            if any(hash in video_hashes[videos[j]] for hash in video_hashes[videos[i]]):
                if videos[i] not in duplicates:
                    duplicates[videos[i]] = []
                duplicates[videos[i]].append(videos[j])

    return duplicates

# Define paths
video_urls_file = '//home/link-lap-24/jupyter_files/duplicate_vide_golf_june7/videos/sample.csv'  # Path to the uploaded CSV file
output_csv_file = 'duplicate_videos.csv'

# Find duplicate videos
duplicates = find_duplicate_videos(video_urls_file)

# Save the results to a CSV file
print("Duplicate videos found:")
with open(output_csv_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Video", "Duplicates"])
    for video, dupes in duplicates.items():
        writer.writerow([video, ",".join(dupes)])
        print(f"{video} has duplicates: {dupes}")

print(f"Output saved to {output_csv_file}")

