from pydantic import BaseModel
from typing import List, Optional

class TrashRequest(BaseModel):
    message_ids: List[str]

class CreateEventRequest(BaseModel):
    summary: str
    start: Optional[str] = None
    duration: int = 30
    location: Optional[str] = None
    description: Optional[str] = None
