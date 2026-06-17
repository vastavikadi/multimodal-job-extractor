import cv2
import os

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval = int(fps)  # 1 frame/sec

    frame_count = 0
    saved = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            cv2.imwrite(
                f"{output_dir}/frame_{saved:03d}.jpg",
                frame
            )
            saved += 1

        frame_count += 1

    cap.release()


reels_dir = "videos"

def execute_frame_extraction():
    os.makedirs(reels_dir, exist_ok=True)
    for filename in os.listdir(reels_dir):
        if filename.endswith(".mp4"):
            video_path = os.path.join(reels_dir, filename)
            reel_id = os.path.splitext(filename)[0]
            output_dir = f"frames/{reel_id}"
            if os.path.exists(output_dir):
                print(f"Frames for {filename} already extracted. Skipping.")
                continue
            extract_frames(video_path, output_dir)
            print(f"Extracted frames from {filename} to {output_dir}")