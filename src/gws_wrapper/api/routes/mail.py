from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage
from gws_wrapper.models.api import TrashRequest

router = APIRouter(prefix="/mail", tags=["mail"])

@router.get("", response_model=List[GmailMessage])
async def list_or_search_messages(q: Optional[str] = None, count: int = 10):
    try:
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

@router.delete("/{message_id}")
async def delete_message(message_id: str):
    try:
        gmail.delete_message(message_id)
        return {"status": "success", "message": f"Deleted {message_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
