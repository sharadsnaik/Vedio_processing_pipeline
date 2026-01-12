from temporalio import activity
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import torch
import os, json

# Load once per worker
PROCESSOR = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
MODEL = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

os.makedirs('Object_detected', exist_ok=True)
MODEL.eval()
output_dir = os.path.join(os.getcwd(), 'detected_Object_')


@activity.defn
async def detect_objects(payload: dict) -> dict:
    frames_dir = payload["frames_dir"]
    confidence_threshold = payload.get("confidence", 0.7)
    

    results = {}

    for img_name in sorted(os.listdir(frames_dir)):
        if not img_name.endswith(".jpg"):
            continue

        img_path = os.path.join(frames_dir, img_name)
        image = Image.open(img_path).convert("RGB")

        inputs = PROCESSOR(images=image, return_tensors="pt")
        outputs = MODEL(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        detections = PROCESSOR.post_process_object_detection(
            outputs, target_sizes=target_sizes, threshold=confidence_threshold
        )[0]

        objects = []
        draw = ImageDraw.Draw(image)

        for box, label, score in zip(
            detections["boxes"], detections["labels"], detections["scores"]
        ):
            label_name = MODEL.config.id2label[label.item()]
            objects.append({"label": label_name, "score": float(score.item())})

            # Draw bounding box
            x0, y0, x1, y1 = box.tolist()
            draw.rectangle([x0, y0, x1, y1], outline="red", width=3)

            # Draw label text
            text = f"{label_name} {score:.2f}"
            draw.text((x0, y0), text, fill="red")

        results[img_name] = objects

        # Save annotated image
        annotated_path = os.path.join(frames_dir, f"annotated_{img_name}")
        image.save(annotated_path)

    # Save results JSON
    results_path = os.path.join(frames_dir, "detections.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    # return {"results_file": results_path, "images_dir": frames_dir}
    return results_path 