import pandas as pd

# Load the CSV files
daily_feedback_df = pd.read_csv("/home/multi-sy-23/Downloads/autoflip/Autoflip_daily_feedback_file - 22-12-2024.csv")
autoflip_df = pd.read_csv("/home/multi-sy-23/Downloads/autoflip/autoflip.csv")

# Create a mapping dictionary for autoflip URLs
url_mapping = dict(zip(autoflip_df['original_input'], autoflip_df['autoflip']))

# Update the 'output url' column in daily_feedback_df
daily_feedback_df['output url'] = daily_feedback_df['video_url'].map(url_mapping).combine_first(daily_feedback_df['output url'])

# Save the updated DataFrame to a new CSV file
daily_feedback_df.to_csv("Updated_Daily_Feedback.csv", index=False)

print("Updated file saved as 'Updated_Daily_Feedback.csv'")

