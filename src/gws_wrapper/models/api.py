from pydantic import BaseModel
from typing import List, Optional

class TrashRequest(BaseModel):
    message_ids: List[str]
