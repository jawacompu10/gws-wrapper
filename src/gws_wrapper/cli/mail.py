import click
from loguru import logger

@click.group()
def mail():
    """Commands related to Gmail services."""
    pass

@mail.command(name="list")
@click.option("--count", default=10, help="Number of messages to list.")
def list_messages(count):
    """List the most recent email messages."""
    logger.info(f"Listing {count} messages...")
    click.echo(f"Structure for listing {count} messages is ready.")
