import click
import json
from loguru import logger
from gws_wrapper.adapters import drive

@click.group()
def drive_group():
    """Commands related to Google Drive services."""
    pass

@drive_group.command(name="search")
@click.argument("query")
@click.option("--limit", type=int, default=10, help="Maximum number of files to return.")
@click.option("--json-output", is_flag=True, help="Output as raw JSON.")
def search(query, limit, json_output):
    """Search for files by name."""
    logger.info(f"Searching for files matching: {query}...")
    
    try:
        files = drive.search_files(query, limit=limit)
        
        if json_output:
            click.echo(json.dumps([f.model_dump() for f in files], indent=2))
        else:
            if not files:
                click.echo("No files found.")
                return

            for f in files:
                click.echo("-" * 40)
                click.echo(f"ID:      {f.id}")
                click.echo(f"Name:    {f.name}")
                click.echo(f"MIME:    {f.mime_type}")
                if f.web_view_link:
                    click.echo(f"URL:     {f.web_view_link}")
            click.echo("-" * 40)
            
    except Exception as e:
        logger.error(f"Failed to search files: {e}")
        raise click.ClickException(str(e))
