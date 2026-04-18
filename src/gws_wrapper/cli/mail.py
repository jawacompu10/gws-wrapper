import click
import json
from typing import List
from loguru import logger
from gws_wrapper.config import settings
from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage

@click.group()
def mail():
    """Commands related to Gmail services."""
    pass

def print_messages(messages: List[GmailMessage], json_output: bool):
    """Shared helper to print message lists."""
    if json_output:
        click.echo(json.dumps([m.model_dump() for m in messages], indent=2))
    else:
        if not messages:
            click.echo("No messages found.")
            return
            
        for msg in messages:
            click.echo("-" * 40)
            click.echo(f"ID:      {msg.id}")
            click.echo(f"From:    {msg.sender or 'N/A'}")
            click.echo(f"Subject: {msg.subject or 'N/A'}")
            click.echo(f"Date:    {msg.date or 'N/A'}")
            click.echo(f"Snippet: {msg.snippet or 'N/A'}")
        click.echo("-" * 40)

@mail.command(name="list")
@click.option("--count", type=int, help="Number of messages to list.")
@click.option("--json-output", is_flag=True, help="Output as raw JSON.")
def list_messages(count, json_output):
    """List the most recent email messages with metadata."""
    count = count or settings.mail.default_count
    logger.info(f"Fetching {count} messages with metadata...")
    try:
        messages = gmail.list_messages(count)
        print_messages(messages, json_output)
    except Exception as e:
        logger.error(f"Failed to list messages: {e}")
        raise click.ClickException(str(e))

@mail.command(name="search")
@click.argument("query")
@click.option("--count", type=int, help="Number of messages to retrieve.")
@click.option("--json-output", is_flag=True, help="Output as raw JSON.")
def search(query, count, json_output):
    """Search messages using Gmail query syntax (e.g., 'from:me', 'subject:test')."""
    count = count or settings.mail.default_count
    logger.info(f"Searching for '{query}' (limit: {count})...")
    try:
        messages = gmail.search_messages(query, count)
        print_messages(messages, json_output)
    except Exception as e:
        logger.error(f"Failed to search messages: {e}")
        raise click.ClickException(str(e))

@mail.command(name="get-body")
@click.argument("message_id")
def get_body(message_id):
    """Get the full body of a specific message."""
    logger.info(f"Fetching body for message {message_id}...")
    try:
        body = gmail.get_message_body(message_id)
        click.echo("-" * 40)
        click.echo(body)
        click.echo("-" * 40)
    except Exception as e:
        logger.error(f"Failed to get message body: {e}")
        raise click.ClickException(str(e))

@mail.command(name="delete")
@click.argument("message_id")
@click.option("--force", is_flag=True, help="Skip confirmation prompt.")
def delete(message_id, force):
    """Permanently delete a specific message."""
    if not force:
        if not click.confirm(f"Are you sure you want to PERMANENTLY delete message {message_id}?"):
            click.echo("Deletion cancelled.")
            return

    logger.info(f"Deleting message {message_id}...")
    try:
        gmail.delete_message(message_id)
        click.echo(f"Successfully deleted message {message_id}.")
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")
        raise click.ClickException(str(e))

@mail.command(name="trash")
@click.argument("message_ids", nargs=-1, required=True)
def trash(message_ids):
    """Move one or more messages to the trash."""
    logger.info(f"Moving {len(message_ids)} messages to trash...")
    try:
        for mid in message_ids:
            gmail.trash_message(mid)
            click.echo(f"Successfully moved message {mid} to trash.")
    except Exception as e:
        logger.error(f"Failed to trash message(s): {e}")
        raise click.ClickException(str(e))

@mail.command(name="archive")
@click.argument("message_ids", nargs=-1, required=True)
def archive(message_ids):
    """Archive one or more messages (removes from Inbox)."""
    logger.info(f"Archiving {len(message_ids)} messages...")
    try:
        for mid in message_ids:
            gmail.archive_message(mid)
            click.echo(f"Successfully archived message {mid}.")
    except Exception as e:
        logger.error(f"Failed to archive message(s): {e}")
        raise click.ClickException(str(e))
