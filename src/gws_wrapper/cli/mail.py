import click
import json
from loguru import logger
from gws_wrapper.config import settings
from gws_wrapper.adapters import gmail

@click.group()
def mail():
    """Commands related to Gmail services."""
    pass

@mail.command(name="list")
@click.option("--count", type=int, help="Number of messages to list.")
@click.option("--json-output", is_flag=True, help="Output as raw JSON.")
def list_messages(count, json_output):
    """List the most recent email messages with metadata."""
    count = count or settings.mail.default_count
    
    logger.info(f"Fetching {count} messages with metadata...")
    
    try:
        messages = gmail.list_messages(count)
        
        if json_output:
            # Use Pydantic's serialization
            click.echo(json.dumps([m.model_dump() for m in messages], indent=2))
        else:
            for msg in messages:
                click.echo("-" * 40)
                click.echo(f"From:    {msg.sender or 'N/A'}")
                click.echo(f"Subject: {msg.subject or 'N/A'}")
                click.echo(f"Date:    {msg.date or 'N/A'}")
                click.echo(f"Snippet: {msg.snippet or 'N/A'}")
            click.echo("-" * 40)
            
    except Exception as e:
        logger.error(f"Failed to list messages: {e}")
        raise click.ClickException(str(e))
