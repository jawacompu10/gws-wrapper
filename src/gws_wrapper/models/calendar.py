from pydantic import BaseModel, ConfigDict
from typing import Optional

class CalendarEvent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    summary: str
    start: str
    end: str
    location: Optional[str] = None
    description: Optional[str] = None
