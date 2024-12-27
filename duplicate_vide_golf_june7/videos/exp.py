import os
import cv2
import imagehash
from PIL import Image
from collections import defaultdict

def extract_key_frames(video_path, num_frames=10):
    """
    Extract key frames from a video.
    
    Args:
        video_path (str): Path to the video file.
        num_frames (int): Number of key frames to extract.
    
    Returns:
        List of PIL Image objects representing the key frames.
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if frame_count == 0:
        raise ValueError("The video contains no frames.")
    
    frame_interval = max(1, frame_count // num_frames)  # Ensure frame_interval is at least 1
    frames = []

    for i in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame))
    
    cap.release()
    return frames

def compute_video_hashes(video_path, num_frames=10):
    """
    Compute perceptual hashes for key frames of a video.
    
    Args:
        video_path (str): Path to the video file.
        num_frames (int): Number of key frames to use for hashing.
    
    Returns:
        List of hashes for the key frames.
    """
    frames = extract_key_frames(video_path, num_frames)
    return [imagehash.phash(frame) for frame in frames]

def find_duplicate_videos(video_folder, num_frames=10, hash_threshold=5):
    """
    Find duplicate videos in a folder based on perceptual hashing.
    
    Args:
        video_folder (str): Path to the folder containing videos.
        num_frames (int): Number of key frames to use for hashing.
        hash_threshold (int): Maximum Hamming distance between hashes to consider videos as duplicates.
    
    Returns:
        List of tuples representing pairs of duplicate videos.
    """
    video_hashes = {}
    duplicates = []

    for video_name in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_name)
        if os.path.isfile(video_path):
            video_hashes[video_name] = compute_video_hashes(video_path, num_frames)

    checked_pairs = set()

    for video1, hashes1 in video_hashes.items():
        for video2, hashes2 in video_hashes.items():
            if video1 != video2 and (video2, video1) not in checked_pairs:
                distances = [hash1 - hash2 for hash1, hash2 in zip(hashes1, hashes2)]
                avg_distance = sum(distances) / len(distances)
                if avg_distance <= hash_threshold:
                    duplicates.append((video1, video2))
                checked_pairs.add((video1, video2))

    return duplicates

# Usage example:
video_folder = "/home/link-lap-24/jupyter_files/duplicate_vide_golf_june7/videos/"  # Replace with the actual path to your video folder

# This function call will find duplicate videos in the specified folder
duplicates = find_duplicate_videos(video_folder)

print("Duplicate videos:", duplicates)

