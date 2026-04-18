from pydantic import BaseModel, ConfigDict
from typing import Optional

class DriveFile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
    mime_type: str
    kind: str
    web_view_link: Optional[str] = None
