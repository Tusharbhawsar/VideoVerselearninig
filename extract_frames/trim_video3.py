import cv2

def trim_video(video_path, output_prefix):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    trimming = False
    start_frame = 0
    trimmed_frames = []
    clip_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if trimming:
            trimmed_frames.append(frame)

            # Add text to the frame
            cv2.putText(frame, f"Trimming Clip {clip_count + 1}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Trim Video', frame)

        key = cv2.waitKey(25) & 0xFF

        if key == ord('s'):
            trimming = True
            start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            trimmed_frames = []
            print(f"Trimming Clip {clip_count + 1} - Start")

        elif key == ord('e'):
            if trimming:
                trimming = False
                end_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                trimmed_frames = trimmed_frames[start_frame - 1:end_frame]
                clip_count += 1
                print(f"Trimming Clip {clip_count} - End")

                # Save the trimmed clip
                out = cv2.VideoWriter(f"{output_prefix}_clip{clip_count}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

                for trimmed_frame in trimmed_frames:
                    out.write(trimmed_frame)

                out.release()

        elif key == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "/home/link-lap-24/ayush/1696917788.mp4"
    output_prefix = "output_trimmed"

    trim_video(video_path, output_prefix)

