import click
from gws_wrapper.cli.mail import mail

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """Google Workspace CLI Wrapper."""
    pass

cli.add_command(mail)

if __name__ == "__main__":
    cli()
