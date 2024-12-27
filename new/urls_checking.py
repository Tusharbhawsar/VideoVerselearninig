# import pandas as pd
# import requests

# # Load the CSV file
# df = pd.read_csv("/home/link-lap-24/timestamp/urls_check397_446.csv")
# urls = df["url"]

# # Function to check URL
# def check_url(url):
#     try:
#         response = requests.get(url, timeout=2)
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except requests.exceptions.RequestException:
#         return False

# # List to hold non-working URLs
# non_working_urls = []
# # non_working_urls.to_csv("non.csv")

# # Check each URL
# for url in urls:
#     if not check_url(url):
#         non_working_urls.append(url)

# # Output the non-working URLs
# print("Non-working URLs:")
# for url in non_working_urls:
#     print(url)
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the CSV file
df = pd.read_csv("/home/link-lap-24/timestamp/1538_1648_fill.csv")
urls = df["url"]

# Function to check URL
def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return url, response.status_code == 200
    except requests.exceptions.RequestException:
        return url, False

# List to hold non-working URLs
non_working_urls = []

# Use ThreadPoolExecutor to check URLs in parallel
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(check_url, url): url for url in urls}
    for future in as_completed(futures):
        url, is_working = future.result()
        if not is_working:
            non_working_urls.append(url)

# Output the non-working URLs
print("Non-working URLs:")
for url in non_working_urls:
    print(url)

