import os
# folderPath = "/home/multi-sy-008/videoverse/tracknetTestData/aceTagged/doubles"
for files in sorted(os.listdir()):
    print(files)
    folder = files.split(".")[0]
    os.mkdir(folder)
    os.system(f" cd {folder}")
    os.system(f"ffmpeg -i {files} '{folder}/%04d.png'")

    print(files, "Done")

