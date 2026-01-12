from temporalio import activity
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer
from PIL import Image
import lancedb
import os
from datetime import datetime

# Load models once
CAPTION_PROCESSOR = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
CAPTION_MODEL = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

@activity.defn
async def caption_embed_store(payload: dict) -> dict:
    frames_dir = payload["frames_dir"]
    detections = payload["detections"]
    lancedb_uri = payload["lancedb_uri"]

    db = lancedb.connect(lancedb_uri)

    if "frame_semantics" in db.table_names():
        table = db.open_table("frame_semantics")
    else:
        table = db.create_table(
            "frame_semantics",
            data=[{
                "image": "",
                "caption": "",
                "objects": [],
                "embedding": [],
                "created_at": "",
            }],
        )

    processed = 0

    for img_name, objects in detections.items():
        img_path = os.path.join(frames_dir, img_name)
        image = Image.open(img_path).convert("RGB")

        inputs = CAPTION_PROCESSOR(image, return_tensors="pt")
        out = CAPTION_MODEL.generate(**inputs)
        caption = CAPTION_PROCESSOR.decode(out[0], skip_special_tokens=True)

        embedding = EMBED_MODEL.encode(caption).tolist()

        record = {
            "image": img_name,
            "caption": caption,
            "objects": objects,
            "embedding": embedding,
            "created_at": datetime.utcnow().isoformat(),
        }

        table.add([record])
        processed += 1

    return {"frames_processed": processed}
