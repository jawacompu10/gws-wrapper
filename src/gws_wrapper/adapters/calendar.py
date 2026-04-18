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

def create_event(summary: str, start_time: str, end_time: str, location: str = None, description: str = None, dry_run: bool = False) -> CalendarEvent:
    """
    Create a new event in the primary calendar.
    """
    body = {
        "summary": summary,
        "start": {"dateTime": start_time},
        "end": {"dateTime": end_time}
    }
    if location:
        body["location"] = location
    if description:
        body["description"] = description

    response = run_gws_command(
        service="calendar",
        resource="events",
        method="insert",
        params={"calendarId": "primary"},
        body=body,
        dry_run=dry_run
    )
    
    # In dry-run mode, gws might return empty or simplified response
    if dry_run:
        return CalendarEvent(
            id="dry-run-id",
            summary=summary,
            start=start_time,
            end=end_time,
            location=location,
            description=description
        )
    
    start = response.get("start", {}).get("dateTime") or response.get("start", {}).get("date")
    end = response.get("end", {}).get("dateTime") or response.get("end", {}).get("date")

    return CalendarEvent(
        id=response["id"],
        summary=response.get("summary", "No Title"),
        start=start,
        end=end,
        location=response.get("location"),
        description=response.get("description")
    )
