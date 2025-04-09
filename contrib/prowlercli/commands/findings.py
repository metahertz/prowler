# prowlercli/commands/findings.py
import click
from prowlercli.client import APIClient

# Group for `prowler findings` related subcommands
@click.group()
def cli():
    """Findings commands"""
    pass

# `prowler findings list` command
def list_findings(inserted_at):
    """List findings"""
    client = APIClient()  # Create API client instance
    params = {}

    # Add filter if provided
    if inserted_at:
        params["filter[inserted_at]"] = inserted_at

    # Call API and display results
    data = client.get("/api/v1/findings", params=params)
    for item in data.get("data", []):
        print(f"- {item['id']}: {item['attributes'].get('check_id', 'N/A')}")

# Register `list` as subcommand under findings
@cli.command("list")
@click.option('--inserted_at', help='Date to filter findings by')
def wrapper(inserted_at):
    list_findings(inserted_at)
