# prowlercli/commands/schedules.py
import click
from prowlercli.client import APIClient

@click.group()
def cli():
    """Schedule management commands"""
    pass

@cli.group("daily")
def daily():
    """Manage daily schedules"""
    pass

@daily.command("list")
def list_daily():
    """List all daily schedules"""
    client = APIClient()
    data = client.get("/api/v1/schedules/daily")
    for item in data.get("data", []):
        attrs = item["attributes"]
        click.echo(f"- {item['id']}: {attrs.get('name', 'Unnamed Schedule')}")
        click.echo(f"  Time: {attrs.get('time')}")
        click.echo(f"  Status: {attrs.get('status', 'unknown')}")
        click.echo(f"  Created: {attrs.get('inserted_at')}")

@daily.command("get")
@click.argument("schedule_id")
def get_daily(schedule_id):
    """Get details of a specific daily schedule"""
    client = APIClient()
    data = client.get(f"/api/v1/schedules/daily/{schedule_id}")
    attrs = data["data"]["attributes"]
    
    click.echo(f"Daily Schedule Details:")
    click.echo(f"ID: {data['data']['id']}")
    click.echo(f"Name: {attrs.get('name', 'Unnamed Schedule')}")
    click.echo(f"Time: {attrs.get('time')}")
    click.echo(f"Status: {attrs.get('status', 'unknown')}")
    click.echo(f"Created: {attrs.get('inserted_at')}")
    click.echo(f"Updated: {attrs.get('updated_at')}")
    
    if "relationships" in data["data"]:
        if "provider" in data["data"]["relationships"]:
            provider_id = data["data"]["relationships"]["provider"]["data"]["id"]
            click.echo(f"Provider ID: {provider_id}") 