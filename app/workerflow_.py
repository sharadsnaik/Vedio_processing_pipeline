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
import os

path_ = os.path.join(f"/tmp", 'video_id.mp4')
lancedb_path = os.path.join(os.getcwd(), "lancedb_OUTS")
# vedio downlaoding workflow
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


        recognition_result = await workflow.execute_activity(
        #   "recognize_frames",
        "detect_objects",
          {
        "frames_dir": frames_out,
            #   "output_txt": f"C:/temp/{video_id}_detections.txt",
              "lancedb_path": lancedb_path,
              
          },
          start_to_close_timeout=timedelta(minutes=10), )
        # return {
               
        #        "recognition": recognition_result,
        # }



        semantic_result = await workflow.execute_activity(
           "caption_embeding_store",
          {
        "frames_dir": f"C:/temp/{video_id}_frames",
        "detections": recognition_result,
        "lancedb_uri": lancedb_path,  },
        start_to_close_timeout=timedelta(minutes=10),
        )
        return semantic_result