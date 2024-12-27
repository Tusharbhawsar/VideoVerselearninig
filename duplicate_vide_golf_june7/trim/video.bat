for %%a in *.mp4 do ffmpeg -i "%%a" -ss 05 -acodec copy -vcodec copy "newfiles\%%~na.avi"
pause
