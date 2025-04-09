# prowlercli/commands/providers.py
import click
from prowlercli.client import APIClient

@click.group()
def cli():
    """Provider management commands"""
    pass

@cli.command("list")
@click.option('--provider-type', help='Filter by provider type (e.g. aws, azure, gcp)')
def list_providers(provider_type):
    """List all providers"""
    client = APIClient()
    params = {}
    if provider_type:
        params["filter[provider]"] = provider_type
    
    data = client.get("/api/v1/providers", params=params)
    for item in data.get("data", []):
        attrs = item["attributes"]
        connection = attrs["connection"]
        click.echo(f"- {item['id']}:") 
        click.echo(f"  Provider-Side ID: {attrs.get('uid')} ({attrs.get('provider')})")
        click.echo(f"  Alias: {attrs.get('alias', 'client-no-data')}")
        click.echo(f"  Created: {attrs.get('inserted_at')}")
        click.echo(f"  Provider Connection: {connection.get('connected', 'client-no-data')}")
        click.echo(f"  Connection Last Checked: {connection.get('last_checked_at', 'client-no-data')}")

@cli.command("get")
@click.argument("provider_id")
def get_provider(provider_id):
    """Get details of a specific provider"""
    client = APIClient()
    data = client.get(f"/api/v1/providers/{provider_id}")
    attrs = data["data"]["attributes"]
    connection = attrs["connection"]
    
    click.echo(f"Provider Details:")
    click.echo(f"- {item['id']}:") 
    click.echo(f"  Provider-Side ID: {attrs.get('uid')} ({attrs.get('provider')})")
    click.echo(f"  Alias: {attrs.get('alias', 'client-no-data')}")
    click.echo(f"  Created: {attrs.get('inserted_at')}")
    click.echo(f"  Provider Connection: {connection.get('connected', 'client-no-data')}")
    click.echo(f"  Connection Last Checked: {connection.get('last_checked_at', 'client-no-data')}")


@cli.group("secrets")
def secrets():
    """Manage provider secrets"""
    pass

@secrets.command("list")
def list_secrets():
    """List all provider secrets"""
    client = APIClient()
    data = client.get("/api/v1/providers/secrets")
    for item in data.get("data", []):
        attrs = item["attributes"]
        related = item["relationships"]
        click.echo(f"- {item['id']}: ")
        click.echo(f"  Friendly Name: {attrs.get('name')}")
        click.echo(f"  Secret Type: {attrs.get('secret_type')}")
        click.echo(f"  Created: {attrs.get('inserted_at')}")
        click.echo(f"  Updated: {attrs.get('updated_at')}")
        click.echo(f"  Linked to provider: {related.get('provider', {}).get('data', {}).get('id')}")

@secrets.command("get")
@click.argument("secret_id")
def get_secret(secret_id):
    """Get details of a specific provider secret"""
    client = APIClient()
    data = client.get(f"/api/v1/providers/secrets/{secret_id}")
    attrs = data["data"]["attributes"]

    related = data["data"]["relationships"]
    click.echo(f"  Friendly Name: {attrs.get('name')}")
    click.echo(f"  Secret Type: {attrs.get('secret_type')}")
    click.echo(f"  Created: {attrs.get('inserted_at')}")
    click.echo(f"  Updated: {attrs.get('updated_at')}")
    click.echo(f"  Linked to provider: {related.get('provider', {}).get('data', {}).get('id')}")