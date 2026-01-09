from pydantic import BaseModel, HttpUrl
from typing import List, Dict

class VedioIngestRequests(BaseModel):
    vedio_id :str
    scr_url: HttpUrl
    