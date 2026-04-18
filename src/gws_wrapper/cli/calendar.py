import click
import json
from loguru import logger
from gws_wrapper.config import settings
from gws_wrapper.adapters import calendar

@click.group()
def calendar_group():
    """Commands related to Google Calendar services."""
    pass

@calendar_group.command(name="list")
@click.option("--days", type=int, help="Number of days to list events for.")
@click.option("--json-output", is_flag=True, help="Output as raw JSON.")
def list_events(days, json_output):
    """List upcoming calendar events."""
    days = days or settings.calendar.default_days
    
    logger.info(f"Fetching calendar events for the next {days} days...")
    
    try:
        events = calendar.list_events(days)
        
        if json_output:
            click.echo(json.dumps([e.model_dump() for e in events], indent=2))
        else:
            if not events:
                click.echo("No upcoming events found.")
                return

            for event in events:
                click.echo("-" * 40)
                click.echo(f"Summary:  {event.summary}")
                click.echo(f"Start:    {event.start}")
                click.echo(f"End:      {event.end}")
                if event.location:
                    click.echo(f"Location: {event.location}")
            click.echo("-" * 40)
            
    except Exception as e:
        logger.error(f"Failed to list events: {e}")
        raise click.ClickException(str(e))

@calendar_group.command(name="create")
@click.argument("summary")
@click.option("--start", help="Start time (ISO 8601 or natural language if gws supports it). Defaults to now.")
@click.option("--duration", type=int, default=30, help="Duration in minutes. Defaults to 30.")
@click.option("--location", help="Event location.")
@click.option("--description", help="Event description.")
def create(summary, start, duration, location, description):
    """Create a new calendar event."""
    from datetime import datetime, timedelta, timezone
    from dateutil import parser
    
    # Parse start time
    if start:
        try:
            start_dt = parser.parse(start)
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
        except Exception as e:
            raise click.BadParameter(f"Invalid start time: {e}")
    else:
        start_dt = datetime.now(timezone.utc)

    end_dt = start_dt + timedelta(minutes=duration)
    
    logger.info(f"Creating event: {summary} at {start_dt.isoformat()} for {duration} mins...")
    
    try:
        event = calendar.create_event(
            summary=summary,
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            location=location,
            description=description
        )
        click.echo(f"Successfully created event: {event.summary} (ID: {event.id})")
        click.echo(f"Start: {event.start}")
        click.echo(f"End:   {event.end}")
    except Exception as e:
        logger.error(f"Failed to create event: {e}")
        raise click.ClickException(str(e))
