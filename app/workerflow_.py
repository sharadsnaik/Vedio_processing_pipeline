from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
import os

path_ = os.path.join(f"/tmp", 'video_id.mp4')
lancedb_path = os.path.join(os.getcwd(), "lancedb_OUTS")
path_tes_ = os.path.join(os.getcwd(),"video_data//ff.mp4")
print(path_tes_)


@workflow.defn
class VideoPipelineWorkflow:

    @workflow.run
    async def run(self, url: str,video_id):
        path = await workflow.execute_activity(
            "download_video",
            {
                "url": url,
                "video_id": video_id

            },
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(
        initial_interval=1,
        maximum_interval=60,
        maximum_attempts=5,
    ),
            
        )
        
    
        # # return path
        frames_out = await workflow.execute_activity(
            "extract_frames",
            {
                "video_path": path,
                "every_n_frames": 30,
            },
            start_to_close_timeout=timedelta(minutes=5),
        )

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

        result = await workflow.execute_activity(
            "analyze_image",
            {"frames_dir":frames_out},
            schedule_to_close_timeout=timedelta(minutes=10)
        )
        return result