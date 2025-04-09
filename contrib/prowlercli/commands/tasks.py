# prowlercli/commands/tasks.py
import click
from prowlercli.client import APIClient

@click.group()
def cli():
    """Task management commands"""
    pass

@cli.command("list")
@click.option('--status', help='Filter by task status')
@click.option('--provider-id', help='Filter by provider ID')
def list_tasks(status, provider_id):
    """List all tasks"""
    client = APIClient()
    params = {}
    
    if status:
        params["filter[status]"] = status
    if provider_id:
        params["filter[provider]"] = provider_id
    
    data = client.get("/api/v1/tasks", params=params)
    for item in data.get("data", []):
        attrs = item["attributes"]
        click.echo(f"- {item['id']}: {attrs.get('name', 'Unnamed Task')}")
        click.echo(f"  Status: {attrs.get('status', 'unknown')}")
        click.echo(f"  Started: {attrs.get('started_at')}")
        click.echo(f"  Completed: {attrs.get('completed_at', 'Not completed')}")

@cli.command("get")
@click.argument("task_id")
def get_task(task_id):
    """Get details of a specific task"""
    client = APIClient()
    data = client.get(f"/api/v1/tasks/{task_id}")
    attrs = data["data"]["attributes"]
    
    click.echo(f"Task Details:")
    click.echo(f"ID: {data['data']['id']}")
    click.echo(f"Name: {attrs.get('name', 'Unnamed Task')}")
    click.echo(f"Status: {attrs.get('status', 'unknown')}")
    click.echo(f"Started: {attrs.get('started_at')}")
    click.echo(f"Completed: {attrs.get('completed_at', 'Not completed')}")
    click.echo(f"Created: {attrs.get('inserted_at')}")
    click.echo(f"Updated: {attrs.get('updated_at')}")
    
    if "relationships" in data["data"]:
        if "provider" in data["data"]["relationships"]:
            provider_id = data["data"]["relationships"]["provider"]["data"]["id"]
            click.echo(f"Provider ID: {provider_id}")
        if "schedule" in data["data"]["relationships"]:
            schedule_id = data["data"]["relationships"]["schedule"]["data"]["id"]
            click.echo(f"Schedule ID: {schedule_id}") 