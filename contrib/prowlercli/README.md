# Prowler CLI

VERSION: Alpha 0.1

This is a *WORK IN PROGRESS* command-line interface for interacting with the Prowler API.
The aim of the CLI is twofold:
    - To allow humans to easily test new features before they are fully supported in the APP/UI.
      - For example, password changes for a user account without three API calls.
      - Listing of UUID's for Providers/Secrets
    - To allow power users to access the data directly, or configure providers without the UI or CURL'ing the API's

# Roadmap
The CLI will follow the API spec fairly closely, with command and subcommands for providers, schedues, tasks, findings, users, etc.
The CLI may pull data from other sections in future to augment output (For example, resolving schedules and tasks to provider friendly names)
Currently, only basic user, tasks, schedules, roles and findings are supported for viewing.
User profile data is the only modifiable option.

## Installation

```bash
# Clone the repository
git clone https://github.com/prowler/prowler.git

# Navigate to the contrib directory
cd prowler/contrib/prowlercli

# Run the module without installation. There is currently no setup.py
python3 -m prowlercli help
python3 -m prowlercli login
```

## Authentication

Before using the CLI, you need to authenticate:

```bash
prowlercli login
```

This will prompt you for your credentials and save the authentication token for subsequent requests.

## Usage

### User Management

View and manage user information:

```bash
# Get current user information
prowlercli users me

# Get user information including roles
prowlercli users me --include-roles

# Update user information
prowlercli users update --name "John Doe" --email "john@example.com"

# List available roles
prowlercli users roles
```

### Provider Management

View and manage cloud providers:

```bash
# List all providers
prowlercli providers list

# List providers of a specific type
prowlercli providers list --provider-type aws

# Get details of a specific provider
prowlercli providers get <provider-id>

# Test connection to a provider
prowlercli providers test-connection <provider-id>

# List provider secrets
prowlercli providers secrets list

# Get details of a specific secret
prowlercli providers secrets get <secret-id>
```

### Schedule Management

Manage scanning schedules:

```bash
# List all daily schedules
prowlercli schedules daily list

# Get details of a specific daily schedule
prowlercli schedules daily get <schedule-id>
```

### Task Management

Monitor and manage scanning tasks:

```bash
# List all tasks
prowlercli tasks list

# List tasks with specific status
prowlercli tasks list --status running

# List tasks for a specific provider
prowlercli tasks list --provider-id <provider-id>

# Get details of a specific task
prowlercli tasks get <task-id>
```

### Findings Management

View security findings:

```bash
# List all findings
prowlercli findings list

# List findings for a specific date
prowlercli findings list --inserted_at 2024-03-20
```

## Environment Variables

The CLI respects the following environment variables:
- `PROWLER_API_URL`: Base URL for the Prowler API
- `PROWLER_TOKEN`: Authentication token (set automatically by `prowlercli login`)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of APACHE2 licence