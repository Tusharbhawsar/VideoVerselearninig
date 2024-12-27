import csv
import os
import requests
import time

download_dir = '/home/link-lap-24/yolov5e/cr'
urls = []
with open('/home/link-lap-24/yolov5e/cric.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        urls.append(row['Source Url'])

print(urls)

failed_urls = urls

while failed_urls:
    new_failed_urls = []

    for url in failed_urls:
        response = os.system(f'wget -P {download_dir} {url}')
        if response != 0:
            new_failed_urls.append(url)
        #time.sleep(1.5)

    failed_urls = new_failed_urls

if failed_urls:
    print("Failed to download the following URLs after all attempts:")
    for url in failed_urls:
        print(url)
