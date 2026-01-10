#worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from app.workerflow_ import VideoPipelineWorkflow
# from app.activities import (
#     # download_video,
#     extract_and_analyze,
#     index_events,
#     store_events,
# )
from app.ingest_vedio import download_video
from app.clickhouse_store_event import store_events
from app.extract_frames import extract_frames
from app.recognize_frames import recognize_frames

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="video-pipeline",
        workflows=[VideoPipelineWorkflow],
        activities=[
            # download_video,
            extract_frames,
            recognize_frames
            # store_events,
        ],
    )

    await worker.run()

asyncio.run(main())
