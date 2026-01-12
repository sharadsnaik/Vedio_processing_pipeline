import pyarrow as pa
from temporalio import activity
import cv2
import os
import lancedb
import numpy as np
from datetime import datetime
import pyarrow as pa

# Load labels once (module-level is OK in activity)
LABELS = open("models/coco.names").read().strip().split("\n")

NET = cv2.dnn.readNetFromONNX("models/yolov5m.onnx")

@activity.defn
async def recognize_frames(payload: dict) -> dict:
    frames_dir = payload["frames_dir"]
    # frames_dir = os.path
    # output_txt = payload["output_txt"]
    lancedb_path = payload["lancedb_path"]

    try:
        db = lancedb.connect(lancedb_path)
    except Exception as e:
        raise RuntimeError(f'Failed to connect to LanceDb, {e}')
    
    # try:
    #     table = init_frame_objects_table(db)
    # except Exception as e:
    #     # FAIL FAST — do NOT continue
    #     raise RuntimeError(f"Failed to init LanceDB table: {e}")



    schema = pa.schema([
        pa.field("id", pa.string()),
            pa.field("image", pa.string()),
        pa.field("objects", pa.list_(pa.string())),
            pa.field("timestamp", pa.string()),
    ]    )

   
    if "frame_objects" in db.table_names():
        # db.drop_table("frame_objects")
        table = db.open_table("frame_objects")
       
    else:
        table = db.create_table(
        "frame_objects",
        schema=schema,
    )


    results = []
    os.makedirs(lancedb_path, exist_ok=True) # ensure directory exists 
    recognized_file = os.path.join(lancedb_path, "recognition_results.txt")

    with open(recognized_file, "w", encoding="utf-8") as f:
        for img_name in sorted(os.listdir(frames_dir)):
            if not img_name.endswith(".jpg"):
                continue

            img_path = os.path.join('frames_output', img_name)
            image = cv2.imread(img_path)

            blob = cv2.dnn.blobFromImage(
                image, 1 / 255.0, (640, 640), swapRB=True, crop=False
            )
            NET.setInput(blob)
            outputs = NET.forward()[0]

            detected_objects = []

            for det in outputs:
                confidence = det[4]
                if confidence < 0.4:
                    continue

                class_id = int(np.argmax(det[5:]))
                label = LABELS[class_id]
                detected_objects.append(label)

            # Write to text file
            f.write(f"{img_name}: {', '.join(detected_objects)}\n")

            # Store in LanceDB
            record = {
                "id":img_name,
                "image": img_name,
                "objects": detected_objects,
                "timestamp": datetime.utcnow().isoformat(),
            }
            table.add([record])

            results.append(record)

    return {
        "frames_processed": len(results),
        # "output_txt": output_txt,
        "lancedb_path": lancedb_path,
    }


# def init_frame_objects_table(db):
#     schema = pa.schema([
#         pa.field("id", pa.string()),
#         pa.field("image", pa.string()),
#         pa.field("objects", pa.list_(pa.string())),
#         pa.field("timestamp", pa.string()),
#     ])

#     tables = db.table_names()

#     if "frame_objects" in tables:
#         return db.open_table("frame_objects")

#     return db.create_table(
#         "frame_objects",
#         schema=schema,
#     )

    