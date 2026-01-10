from temporalio import activity
import cv2
import os

@activity.defn
async def extract_frames(payload: dict) -> dict:
    video_path = payload["video_path"]
    # frames_dir = payload["frames_dir"]
    every_n_frames = payload.get("every_n_frames", 30)
    
    frames_dir = 'frames_output'
    os.makedirs(frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    frame_count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % every_n_frames == 0:
            frame_path = os.path.join(frames_dir, f"frame_{saved:05d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved += 1

        frame_count += 1

    cap.release()

    return  frames_dir