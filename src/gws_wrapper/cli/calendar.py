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
