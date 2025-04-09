# prowlercli/commands/users.py
import click
from prowlercli.client import APIClient

@click.group()
def cli():
    """User management commands"""
    pass

@cli.command("me")
@click.option('--include-roles', is_flag=True, help='Include user roles in the output')
def get_current_user(include_roles):
    """Get current user information"""
    client = APIClient()
    params = {
        "fields[users]": "email,name,company_name,date_joined,is_verified"
    }
    if include_roles:
        params["include"] = "roles"
    
    data = client.get("/api/v1/users/me", params=params)
    user = data["data"]["attributes"]
    
    click.echo("Current User Information:")
    click.echo(f"Email: {user.get('email')}")
    click.echo(f"Name: {user.get('name')}")
    click.echo(f"Date Joined: {user.get('date_joined')}")
    click.echo(f"verified_user: {user.get('is_verified')}")
    
    if include_roles and "included" in data:
        click.echo("\nRoles:")
        for role in data["included"]:
            if role["type"] == "roles":
                click.echo(f"- {role['attributes'].get('name')}")

@cli.command("update")
@click.option('--name', help='New Friendly Name')
@click.option('--email', help='New email address')
@click.option('--password', help='Set new user password')
def update_user(name, email, password):
    """Update current user information"""
    if not any([name, password,email]):
        click.echo("Error: At least one field to update must be provided")
        return
    
    client = APIClient()
    # First get current user ID
    current_user = client.get("/api/v1/users/me")
    user_id = current_user["data"]["id"]
    
    # Prepare update data
    attributes = {}
    if name:
        attributes["name"] = name
    if password:
        attributes["password"] = password
    if email:
        attributes["email"] = email
    
    data = {
        "data": {
            "type": "users",
            "id": user_id,
            "attributes": attributes
        }
    }
    
    # Update user using PATCH
    client.patch(f"/api/v1/users/{user_id}", json=data)
    click.echo("User information updated successfully")

@cli.command("roles")
def list_roles():
    """List all available roles"""
    client = APIClient()
    data = client.get("/api/v1/roles")
    
    click.echo("Available Roles:")
    for role in data.get("data", []):
        click.echo(f"- {role['attributes'].get('name')}: {role['attributes'].get('description', 'No description')}") 