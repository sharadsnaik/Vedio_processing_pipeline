import os, json, base64
from openai import OpenAI
from dotenv import load_dotenv
from temporalio import activity

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"]
)

from PIL import Image
import io

def encode_image_small_size(path, max_size=512, quality=60):
    img = Image.open(path).convert("RGB")
    img.thumbnail((max_size, max_size))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


@activity.defn
async def analyze_image(payload: dict) -> dict:
    frames_dir = payload["frames_dir"]
    os.makedirs("Extracted_VLM", exist_ok=True)

    results = {}  # FIXED
    static_image_server = "http://127.0.0.1:8000"

    for img_name in sorted(os.listdir(frames_dir)):
        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # img_path = os.path.join(frames_dir, img_name)
        # image_base64 = encode_image_small_size(img_path)

        image_url = f"{static_image_server}/{img_name}"

        # response = client.responses.create(
        #     model="Qwen/Qwen3-VL-30B-A3B-Instruct",
        #     input=[
        #     {
        #         "type": "image",
        #         "image": image_url,
        #     },
        #     {"type": "text", "text": "Describe this image."},
        # ],)

        response = client.responses.create(
    model="Qwen/Qwen3-VL-30B-A3B-Instruct",
    input=f"""
<image>{image_url}</image>
Describe this image in one sentence.
"""
)


        # print('resposesss', response)

        results[img_name] = response.output_text


    results_path = os.path.join("Extracted_VLM", "image_description.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    # return {"results_file": results_path}
    return {
        "video_id": payload["video_id"],
        "frame_name": img_name,
        "image_url": image_url,
        "description": response.output_text,
        "model": "Qwen/Qwen3-VL-30B-A3B-Instruct"
    }



# Command 'python' not found, did you mean:
#   command 'python3' from deb python3
#   command 'python' from deb python-is-python3
# sharad@shocessing_pipeline/frames_output$ python3 -m http.server 8000
# Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
# 127.0.0.1 - - [13/Jan/2026 14:29:18] code 404, message File not found
# 127.0.0.1 - - [13/Jan/2026 14:29:18] "GET /frame_0001.jpg HTTP/1.1" 404 -
# 127.0.0.1 - - [13/Jan/2026 14:29:18] code 404, message File not found
# 127.0.0.1 - - [13/Jan/2026 14:29:18] "GET /favicon.ico HTTP/1.1" 404 -
# 127.0.0.1 - - [13/Jan/2026 14:30:05] code 404, message File not found
# 127.0.0.1 - - [13/Jan/2026 14:30:05] "GET /frame_0000.jpg HTTP/1.1" 404 -
# 127.0.0.1 - - [13/Jan/2026 14:30:47] "GET /frame_00001.jpg HTTP/1.1" 200 -





