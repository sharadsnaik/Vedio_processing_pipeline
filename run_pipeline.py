import asyncio
from temporalio.client import Client
from app.workerflow_ import VideoPipelineWorkflow


workflow_id = "sample_test"

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
