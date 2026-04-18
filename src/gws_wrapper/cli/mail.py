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
def list_messages(count):
    """List the most recent email messages."""
    # Use config value if not provided via CLI
    count = count or settings.mail.default_count
    
    logger.info(f"Fetching {count} messages...")
    
    try:
        messages = gmail.list_messages(count)
        # For now, just print the JSON output
        click.echo(json.dumps(messages, indent=2))
    except Exception as e:
        logger.error(f"Failed to list messages: {e}")
        raise click.ClickException(str(e))
