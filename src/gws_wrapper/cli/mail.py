import click
from loguru import logger
from gws_wrapper.config import settings

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
    
    logger.info(f"Listing {count} messages...")
    click.echo(f"Structure for listing {count} messages is ready (using config default).")
