from temporalio import activity
import requests
import cv2
import numpy as np
import lancedb
# from sentence_transformers import SentenceTransformer
import clickhouse_connect

# model = SentenceTransformer("all-MiniLM-L6-v2")



@activity.defn
def extract_and_analyze(video_path: str):
    cap = cv2.VideoCapture(video_path)
    prev = None
    events = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ts = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        if prev is not None:
            diff = cv2.absdiff(prev, gray)
            score = float(np.mean(diff))
            events.append({"timestamp": ts, "motion": score})

        prev = gray

    cap.release()
    return events


# @activity.defn
# def index_events(events):
#     db = lancedb.connect("./lancedb")
#     table = db.create_table(
#         "events",
#         data=[{"vector": model.encode(str(e)), **e} for e in events],
#         mode="overwrite"
#     )
#     return True


@activity.defn
def store_events(video_id: str, events):
    client = clickhouse_connect.get_client(host="localhost")
    for e in events:
        client.insert(
            "video_analytics",
            [{
                "video_id": video_id,
                "event_type": "motion",
                "value": e["motion"]
            }]
        )
