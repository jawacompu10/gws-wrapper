from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage
from gws_wrapper.models.api import TrashRequest
from gws_wrapper.config import settings

router = APIRouter(prefix="/mail", tags=["mail"])

@router.get("", response_model=List[GmailMessage])
async def list_or_search_messages(
    q: Optional[str] = None, 
    count: Optional[int] = Query(None, description="Number of messages to retrieve")
):
    try:
        count = count or settings.mail.default_count
        if q:
            return gmail.search_messages(q, count)
        return gmail.list_messages(count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{message_id}")
async def get_message_body(message_id: str):
    try:
        body = gmail.get_message_body(message_id)
        return {"id": message_id, "body": body}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trash")
async def trash_messages(request: TrashRequest):
    try:
        for mid in request.message_ids:
            gmail.trash_message(mid)
        return {"status": "success", "count": len(request.message_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/archive")
async def archive_messages(request: TrashRequest):
    try:
        for mid in request.message_ids:
            gmail.archive_message(mid)
        return {"status": "success", "count": len(request.message_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
