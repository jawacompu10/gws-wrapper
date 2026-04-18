from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import dateparser
from datetime import datetime, timedelta, timezone
from gws_wrapper.adapters import calendar
from gws_wrapper.models.calendar import CalendarEvent
from gws_wrapper.models.api import CreateEventRequest
from gws_wrapper.config import settings

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("", response_model=List[CalendarEvent])
async def list_events(days: Optional[int] = Query(None, description="Number of days to list events for")):
    try:
        days = days or settings.calendar.default_days
        return calendar.list_events(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=CalendarEvent)
async def create_event(request: CreateEventRequest):
    try:
        if request.start:
            start_dt = dateparser.parse(request.start, settings={'PREFER_DATES_FROM': 'future'})
            if not start_dt:
                raise HTTPException(status_code=400, detail="Invalid start time format")
            if start_dt.tzinfo is None:
                start_dt = start_dt.astimezone()
        else:
            start_dt = datetime.now(timezone.utc)

        end_dt = start_dt + timedelta(minutes=request.duration)
        
        return calendar.create_event(
            summary=request.summary,
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            location=request.location,
            description=request.description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
