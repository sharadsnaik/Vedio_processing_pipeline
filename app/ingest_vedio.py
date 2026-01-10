#ingest_vedio
from temporalio import activity
import requests, os

@activity.defn
async def download_video(payload: dict) -> str:
    url = payload["url"]
    video_id = payload["video_id"]
    base_dir = "video_data"
    os.makedirs(base_dir, exist_ok=True)

    out_path = os.path.join(base_dir, f"{video_id}.mp4")


    r = requests.get(url, stream=True)
    r.raise_for_status()

    with open(out_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return out_path
