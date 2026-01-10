import asyncio
from temporalio.client import Client
from app.workerflow_ import VideoPipelineWorkflow
import uuid

workflow_id = f"video-{uuid.uuid4()}"

async def run():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
    VideoPipelineWorkflow.run,
    args=[
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'ff'
        ],
    task_queue="video-pipeline",
    id=workflow_id,
)
    print(result)

asyncio.run(run())
