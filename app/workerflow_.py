from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
import os

path_ = os.path.join(f"/tmp", 'video_id.mp4')
lancedb_path = os.path.join(os.getcwd(), "lancedb_OUTS")
path_tes_ = os.path.join(os.getcwd(),"video_data//ff.mp4")
print(path_tes_)


retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    maximum_interval=timedelta(seconds=60),
    maximum_attempts=5,
)
@workflow.defn
class VideoPipelineWorkflow:
    
    def __init__(self):
        self.paused = False
        self.cancelled = False 
        self.every_n_frames = 30
        self.current_stage = "init"

    @workflow.signal
    async def pause(self):
        self.paused = True
    
    @workflow.signal
    async def resume(self):
        self.paused = False
    
    @workflow.signal
    async def cancel(self):
        self.cancelled = True
    
    @workflow.signal
    async def update_frames_rate(self, every_n_frames:int):
        self.every_n_frames = every_n_frames
    
    # making explicitly state check
    async def _wait_if_paused(self):
        while self.paused:
            await workflow.sleep(2)


    @workflow.run
    async def run(self, url: str,video_id):
        self.current_stage = "download"

        path = await workflow.execute_activity(
            "download_video",
            {
                "url": url,
                "video_id": video_id

            },
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )

        await self._wait_if_paused()
        if self.cancelled:
            return "Cancelled after downlaod"
        
        self.current_stage = "extract_frames"
            
        # # return path
        frames_out = await workflow.execute_activity(
            "extract_frames",
            {
                "video_path": path,
                "every_n_frames": self.every_n_frames,
            },
            start_to_close_timeout=timedelta(minutes=5),
        )

        await self._wait_if_paused()
        if self.cancelled:
            return "Cancelled after frame extraction"

        # return {"result": frames_out,"output_dir": f"C:/temp/{video_id}_frames", "every_n_frames": 30 },


        # recognition_result = await workflow.execute_activity(
        # #   "recognize_frames",
        # "detect_objects",
        #   {
        # "frames_dir": frames_out,
        #     #   "output_txt": f"C:/temp/{video_id}_detections.txt",
        #       "lancedb_path": lancedb_path,
              
        #   },
        #   start_to_close_timeout=timedelta(minutes=10), )
        # # return {
               
        # #        "recognition": recognition_result,
        # # }



        # semantic_result = await workflow.execute_activity(
        #    "caption_embeding_store",
        #   {
        # "frames_dir": f"C:/temp/{video_id}_frames",
        # "detections": recognition_result,
        # "lancedb_uri": lancedb_path,  },
        # start_to_close_timeout=timedelta(minutes=10),
        # )
        # return semantic_result

        self.current_stage = "analyze"

        result = await workflow.execute_activity(
            "analyze_image",
            {"frames_dir":frames_out},
            schedule_to_close_timeout=timedelta(minutes=10)
        )

        self.current_stage = "done"
        return result
    
