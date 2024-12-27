import cv2



video = cv2.VideoCapture("https://dwapv64icf8j2.cloudfront.net/9qHLjwzph/1674200089.mp4")



while True:

    frameNo = int(input())

    video.set(1,frameNo)

    ret,frame = video.read()

    cv2.imshow(f"{frameNo}",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()