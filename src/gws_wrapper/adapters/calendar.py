from datetime import datetime, timedelta, timezone
from typing import List
from gws_wrapper.adapters.cli import run_gws_command
from gws_wrapper.models.calendar import CalendarEvent

def list_events(days: int) -> List[CalendarEvent]:
    """
    Fetch events from the primary calendar for the next N days.
    """
    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=days)).isoformat()

    response = run_gws_command(
        service="calendar",
        resource="events",
        method="list",
        params={
            "calendarId": "primary",
            "timeMin": time_min,
            "timeMax": time_max,
            "singleEvents": True,
            "orderBy": "startTime"
        }
    )

    items = response.get("items", [])
    events = []
    
    for item in items:
        # Start and end can be in 'dateTime' (for specific times) or 'date' (for all-day events)
        start = item.get("start", {}).get("dateTime") or item.get("start", {}).get("date")
        end = item.get("end", {}).get("dateTime") or item.get("end", {}).get("date")
        
        events.append(CalendarEvent(
            id=item["id"],
            summary=item.get("summary", "No Title"),
            start=start,
            end=end,
            location=item.get("location"),
            description=item.get("description")
        ))
        
    return events
