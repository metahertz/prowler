# prowlercli/__main__.py
import click
from prowlercli.commands import findings, login, users, providers, schedules, tasks

# Entry point for the CLI application using Click
@click.group()
def cli():
    """Prowler CLI - Interact with the Prowler API"""
    pass

# Register subcommands explicitly by name
cli.add_command(login.login_command, name="login")
cli.add_command(findings.cli, name="findings")
cli.add_command(users.cli, name="users")
cli.add_command(providers.cli, name="providers")
cli.add_command(schedules.cli, name="schedules")
cli.add_command(tasks.cli, name="tasks")

# Allow this module to be run as a script
if __name__ == '__main__':
    cli()