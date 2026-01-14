import asyncio
from temporalio.client import Client
from app.workerflow_ import VideoPipelineWorkflow

workflow_id = "sample_test"


async def main():
    client = await Client.connect("localhost:7233")

    handle = client.get_workflow_handle(workflow_id)

    # pause
    await handle.signal(VideoPipelineWorkflow.pause)

    # resume
    await handle.signal(VideoPipelineWorkflow.resume)

    # change config
    await handle.signal(VideoPipelineWorkflow.update_frame_rate, 10)

asyncio.run(main())
