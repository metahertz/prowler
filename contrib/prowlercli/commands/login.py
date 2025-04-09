# prowlercli/commands/login.py
import click
from prowlercli import auth

# `prowler login` command definition
@click.command()
def login_command():
    """Authenticate with the Prowler API"""
    auth.login()
