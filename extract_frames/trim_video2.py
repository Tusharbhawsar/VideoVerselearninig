import cv2

def trim_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    trimming = False
    start_frame = 0
    trimmed_frames = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if trimming:
            trimmed_frames.append(frame)

        cv2.imshow('Trim Video', frame)

        key = cv2.waitKey(25) & 0xFF

        if key == ord('s'):
            trimming = True
            start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            trimmed_frames = []

        elif key == ord('e'):
            trimming = False
            end_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            trimmed_frames = trimmed_frames[start_frame - 1:end_frame]

        elif key == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the trimmed video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    for frame in trimmed_frames:
        out.write(frame)

    out.release()

if __name__ == "__main__":
    video_path = "/home/link-lap-24/ayush/1696917788.mp4"
    output_path = "output_trimmed.mp4"

    trim_video(video_path, output_path)

