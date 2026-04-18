import click
from gws_wrapper.cli.mail import mail

@click.group()
def cli():
    """Google Workspace CLI Wrapper."""
    pass

cli.add_command(mail)

if __name__ == "__main__":
    cli()
