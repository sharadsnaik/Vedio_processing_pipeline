# from temporalio import workflow, activity
# from .ingest_vedio import downlaod_vedio

# @workflow.defn
# class VideoPipelineWorkflow:

#     @workflow.run
#     async def run(self, vedio_id: str, url: str):
#         path = await workflow.execute_activity(downlaod_vedio, url, f"/tem/{vedio_id}.mp4", start_to_close_timeout=120)

#         return path
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class VideoPipelineWorkflow:

    @workflow.run
    async def run(self, video_id: str, url: str):
        path = await workflow.execute_activity(
            "download_video",
            url,
            f"/tmp/{video_id}.mp4",
            start_to_close_timeout=timedelta(minutes=2),
        )
        return path

        # events = await workflow.execute_activity(
        #     "extract_and_analyze",
        #     path,
        #     start_to_close_timeout=timedelta(minutes=5),
        # )

        # await workflow.execute_activity(
        #     "index_events",
        #     events,
        #     start_to_close_timeout=timedelta(minutes=2),
        # )

        # await workflow.execute_activity(
        #     "store_events",
        #     video_id,
        #     events,
        #     start_to_close_timeout=timedelta(minutes=2),
        # )

        # return f"Processed {len(events)} events"
