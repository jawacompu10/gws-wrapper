from pydantic import BaseModel
from typing import Optional

class GmailMessage(BaseModel):
    id: str
    thread_id: Optional[str] = None
    sender: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    snippet: Optional[str] = None

    class Config:
        from_attributes = True
