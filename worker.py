#worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from app.workerflow_ import VideoPipelineWorkflow

from app.ingest_vedio import download_video
from app.clickhouse_store_event import store_events
from app.extract_frames import extract_frames
from app.recognize_frames import recognize_frames
from app.recognize_frames_v2 import detect_objects
from app.caption_embeding_store import caption_embed_store
from app.LLM_model import analyze_image

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="video-pipeline",
        workflows=[VideoPipelineWorkflow],
        activities=[
            download_video,
            extract_frames,
            # recognize_frames
            # detect_objects,
            # caption_embed_store,

            analyze_image


        ],
    )

    await worker.run()

asyncio.run(main())
