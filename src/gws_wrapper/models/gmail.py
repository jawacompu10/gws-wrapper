from pydantic import BaseModel, ConfigDict
from typing import Optional

class GmailMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    thread_id: Optional[str] = None
    sender: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    snippet: Optional[str] = None
