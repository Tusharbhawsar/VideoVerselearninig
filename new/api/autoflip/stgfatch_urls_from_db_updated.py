import requests
import json
import pandas as pd

# Step 1: Fetch data from the API
i_value = "yTa-MOQah"
url = f"https://stg.api.magnifi.ai/get/clips/{i_value}?limit=1000&pageNo=1&filters={{\"players\":[],\"events\":[],\"sortBy\":\"TIME_DESCENDANT\",\"aspectRatio\":\"\",\"playBackSpeed\":[],\"webhookPublish\":\"\",\"clipData\":{{}}}}&daterange=[]&sort={{\"start_time\":-1,\"_id\":1}}&type=all&search=&aspectRatio=&webhookPublish=&isManualUpload=false&skipCount="
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    video_urls = []
    input_urls = []
    
    # Step 2: Process API response to extract URLs
    for clip in data['clips']:
        video_url = clip.get('video_url')
        input_url = clip.get("videoUrl")
        edited_videos = clip.get('editedVideos', [])
        
        for edited_clip in edited_videos:
            video_url = edited_clip.get('video_url')
            input_url = edited_clip.get("videoUrl")
            
            if video_url:
                video_urls.append(video_url)
            if input_url:
                input_urls.append(input_url)

    # Save video URLs to video_urls.txt
    with open("video_urls.txt", "w") as video_file:
        for video_url in video_urls:
            video_file.write(f"{video_url}\n")

    # Save input URLs to input_urls.txt
    with open("input_urls.txt", "w") as input_file:
        for input_url in input_urls:
            input_file.write(f"{input_url}\n")

    print("video_urls.txt and input_urls.txt files created successfully.")

    # Step 3: Update the CSV file based on generated files
    football_df = pd.read_csv('/home/multi-sy-23/Downloads/autoflip/d.csv')

    # Read URLs from input_urls.txt and video_urls.txt as lists
    with open('input_urls.txt', 'r') as f:
        input_urls = f.read().splitlines()

    with open('video_urls.txt', 'r') as f:
        video_urls = f.read().splitlines()

    # Create a list to hold the output URLs
    output_urls = []

    # For each URL in the video_url column of the CSV, find the matching line in input_urls.txt
    for video_url in football_df['video_url']:
        # Find the index of the matching URL in input_urls
        if video_url in input_urls:
            matched_index = input_urls.index(video_url)
            # Use the matched index to get the corresponding URL in video_urls
            output_urls.append(video_urls[matched_index])
        else:
            output_urls.append(None)  # If no match is found

    # Insert the output_url column immediately after the video_url column
    video_url_index = football_df.columns.get_loc('video_url')
    football_df.insert(video_url_index + 1, 'output_url', output_urls)

    # Save the updated CSV
    football_df.to_csv('cric.csv', index=False)
    print("football_updated.csv created successfully.")
else:
    print("Failed to retrieve data:", response.status_code)

