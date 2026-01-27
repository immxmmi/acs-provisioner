# ACS Provisioner

Pipeline-based provisioner for **Red Hat Advanced Cluster Security (ACS/StackRox)**.

Automate the configuration of:
- **Auth Providers** (OIDC, SAML, LDAP)
- **Roles & RBAC** (Permission Sets, Access Scopes, Roles)
- **Notifiers** (Slack, Email, Jira, PagerDuty, Splunk)
- **Image Integrations** (Quay, Docker, ECR, GCR, ACR)
- **Security Policies**

## Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your ACS Central URL and API token

# 2. Configure pipeline
# Edit src/pipelines/pipeline.yaml and inputs.yaml

# 3. Run
make run
```

## Local RHACS (ACS) Setup for API Testing

For local development and API testing, this repository includes a dedicated Makefile to spin up **Minikube with Red Hat Advanced Cluster Security (ACS/RHACS)**.

The Makefile is located at:

```
environment/Makefile
```

### Prerequisites

- Docker
- kubectl
- minikube
- curl
- make

### What the Makefile does

The environment Makefile automates the following steps:

- Starts a Minikube cluster with sufficient resources
- Downloads `roxctl` if not present
- Deploys **ACS Central**
- Deploys **Secured Cluster Services**
- Exposes the Central API and UI locally

This setup is intended **only for development and testing**.

### Usage

```bash
cd environment

# Start Minikube and install ACS
make up
```

After deployment:

```bash
# Forward Central UI and API
make ui
```

- UI: https://localhost:8443  
- API base: https://localhost:8443/v1  
- Default user: `admin`

### Tear down

```bash
cd environment
make down
```

### Use with ACS Provisioner

Once ACS is running locally, configure your `.env` file as follows:

```env
API_HOST=localhost
API_PORT=8443
API_BASE_PATH=/
API_AUTH_TYPE=bearer
API_TOKEN=<GENERATED_TOKEN>
DISABLE_TLS_VERIFY=true
```

You can then run the provisioner against the local ACS instance:

```bash
make run
```

This allows full end-to-end testing of:
- ACS API integration
- Pipelines
- Actions (Auth Providers, Roles, Policies, Notifiers, Integrations)

## Local RHACS (ACS) Setup for API Testing

For local development and API testing, this repository includes a dedicated Makefile to spin up **Minikube with Red Hat Advanced Cluster Security (ACS/RHACS)**.

The Makefile is located at:

```
environment/Makefile
```

### Prerequisites

- Docker
- kubectl
- minikube
- curl
- make

### What the Makefile does

The environment Makefile automates the following steps:

- Starts a Minikube cluster with sufficient resources
- Downloads `roxctl` if not present
- Deploys **ACS Central**
- Deploys **Secured Cluster Services**
- Exposes the Central API and UI locally

This setup is intended **only for development and testing**.

### Usage

```bash
cd environment

# Start Minikube and install ACS
make up
```

After deployment:

```bash
# Forward Central UI and API
make ui
```

- UI: https://localhost:8443  
- API base: https://localhost:8443/v1  
- Default user: `admin`

### Tear down

```bash
cd environment
make down
```

### Use with ACS Provisioner

Once ACS is running locally, configure your `.env` file as follows:

```env
API_HOST=localhost
API_PORT=8443
API_BASE_PATH=/
API_AUTH_TYPE=bearer
API_TOKEN=<GENERATED_TOKEN>
DISABLE_TLS_VERIFY=true
```

You can then run the provisioner against the local ACS instance:

```bash
make run
```

This allows full end-to-end testing of:
- ACS API integration
- Pipelines
- Actions (Auth Providers, Roles, Policies, Notifiers, Integrations)

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_HOST` | ACS Central hostname | `central.example.com` |
| `API_PORT` | ACS Central port | `443` |
| `API_BASE_PATH` | API base path | `/` |
| `API_AUTH_TYPE` | Authentication type | `bearer` |
| `API_TOKEN` | ACS API token | `eyJhbGc...` |
| `DISABLE_TLS_VERIFY` | Skip TLS verification | `false` |

### Getting an API Token

1. Log into ACS Central UI
2. Go to **Platform Configuration → Integrations → Authentication Tokens**
3. Click **Generate Token**
4. Select role with appropriate permissions
5. Copy the token to your `.env` file

## Pipeline Structure

```yaml
# pipeline.yaml
pipeline:
  - name: Create Permission Set
    job: create_permission_set
    enabled: true
    params:
      name: "Security-Analyst"
      resource_to_access:
        Alert: READ_ACCESS
        Policy: READ_ACCESS

  - name: Create Notifiers
    job: create_notifier
    enabled: true
    params_list: "{{ notifiers }}"  # Dynamic from inputs.yaml
```

```yaml
# inputs.yaml
notifiers:
  - name: "Slack-Security"
    type: "slack"
    slack:
      webhook: "https://hooks.slack.com/..."
```

## Available Actions

### Auth Providers
- `create_auth_provider` - Create OIDC/SAML/LDAP provider
- `get_auth_provider` - Get provider by name
- `list_auth_providers` - List all providers
- `update_auth_provider` - Update existing provider
- `delete_auth_provider` - Delete provider

### Roles & RBAC
- `create_role` / `get_role` / `list_roles` / `delete_role`
- `create_permission_set` / `get_permission_set` / `list_permission_sets` / `delete_permission_set`
- `create_access_scope` / `get_access_scope` / `list_access_scopes` / `delete_access_scope`

### Notifiers
- `create_notifier` / `get_notifier` / `list_notifiers` / `delete_notifier`
- `test_notifier` - Test notifier configuration

### Image Integrations
- `create_integration` / `get_integration` / `list_integrations` / `delete_integration`

### Policies
- `create_policy` / `get_policy` / `list_policies` / `delete_policy`
- `enable_policy` / `disable_policy`

## Development

```bash
# Run tests
make test

# Run with debug output
make run-debug

# Lint code
make lint

# Build Docker image
make build TAG=1.0.0

# Show all commands
make help
```

## Architecture

```
src/
├── acs/                    # ACS-specific module
│   ├── acs_gateway.py      # ACS API client
│   ├── actions/            # Pipeline actions
│   │   ├── auth_provider/
│   │   ├── role/
│   │   ├── access_scope/
│   │   ├── permission_set/
│   │   ├── notifier/
│   │   ├── integration/
│   │   └── policy/
│   └── model/              # Pydantic models
├── engine/                 # Generic pipeline engine
├── gateway/                # Generic API client
└── pipelines/              # YAML pipeline definitions
```

## Docker

```bash
# Build
make build

# Run
docker run --rm \
  -e API_HOST=central.example.com \
  -e API_TOKEN=your-token \
  -v $(pwd)/pipelines:/app/pipelines \
  acs-provisioner:latest
```

## Helm

```bash
# Install
make helm-install HELM_NAMESPACE=rhacs-system

# Upgrade
make helm-upgrade
```


## Local RHACS (ACS) Setup for API Testing

For local development and API testing, this repository includes a dedicated Makefile to spin up **Minikube with Red Hat Advanced Cluster Security (ACS/RHACS)**.

The Makefile is located at:

```
environment/Makefile
```

### Prerequisites

- Docker
- kubectl
- minikube
- curl
- make

### What the Makefile does

The environment Makefile automates the following steps:

- Starts a Minikube cluster with sufficient resources
- Downloads `roxctl` if not present
- Deploys **ACS Central**
- Deploys **Secured Cluster Services**
- Exposes the Central API and UI locally

This setup is intended **only for development and testing**.

### Usage

```bash
cd environment

# Start Minikube and install ACS
make up
```

After deployment:

```bash
# Forward Central UI and API
make ui
```

- UI: https://localhost:8443  
- API base: https://localhost:8443/v1  
- Default user: `admin`

### Tear down

```bash
cd environment
make down
```

### Use with ACS Provisioner

Once ACS is running locally, configure your `.env` file as follows:

```env
API_HOST=localhost
API_PORT=8443
API_BASE_PATH=/
API_AUTH_TYPE=bearer
API_TOKEN=<GENERATED_TOKEN>
DISABLE_TLS_VERIFY=true
```

You can then run the provisioner against the local ACS instance:

```bash
make run
```

This allows full end-to-end testing of:
- ACS API integration
- Pipelines
- Actions (Auth Providers, Roles, Policies, Notifiers, Integrations)
