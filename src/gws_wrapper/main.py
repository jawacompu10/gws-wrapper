import click
from gws_wrapper.cli.mail import mail
from gws_wrapper.cli.calendar import calendar_group
from gws_wrapper.cli.drive import drive_group

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """Google Workspace CLI Wrapper."""
    pass

cli.add_command(mail)
cli.add_command(calendar_group, name="calendar")
cli.add_command(drive_group, name="drive")

if __name__ == "__main__":
    cli()
