import asyncio
from temporalio.client import Client

async def run():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        "VideoPipelineWorkflow",
        "https://youtu.be/KSP4o_WCqVs?si=YZe45Hzfds74OhMn",
        task_queue="video-pipeline",
        id="video-1"
    )
    print(result)

asyncio.run(run())