# ACS Provisioner

Pipeline-based provisioner for **Red Hat Advanced Cluster Security (ACS/StackRox)**.

Automate the configuration of:
- **Auth Providers** (OIDC, SAML, LDAP)
- **Roles & RBAC** (Permission Sets, Access Scopes, Roles)
- **Notifiers** (Jira, Email, Splunk, Syslog, PagerDuty, Generic Webhook, CSCC, Sumologic, AWS Security Hub, Microsoft Sentinel)
- **Image Integrations** (Quay, Docker, ECR, GCR, ACR)
- **Security Policies**

## Quick Start

```bash
# 1. Setup
make setup
source .venv/bin/activate

# 2. Configure environment
cp .env.example .env
# Edit .env with your ACS Central URL and API token

# 3. Configure pipeline
# Edit src/pipelines/pipeline.yaml and inputs.yaml

# 4. Run
make run
```

## Available Make Commands

```bash
make help          # Show all commands

# Main
make run           # Run the provisioner
make run-debug     # Run with debug logging
make test          # Run tests
make test-models   # Test model imports

# Setup
make install       # Install dependencies
make venv          # Create virtual environment
make setup         # Full setup (venv + install)

# Development
make lint          # Run linter
make format        # Format code with black
make clean         # Clean cache files

# Docker
make build         # Build Docker image
make docker-run    # Run in Docker

# RHACS Environment (Minikube)
make env-up        # Start Minikube with ACS
make env-down      # Stop Minikube
make env-status    # Show ACS pod status
make env-ui        # Port-forward ACS UI
```

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
2. Go to **Platform Configuration > Integrations > Authentication Tokens**
3. Click **Generate Token**
4. Select role with appropriate permissions
5. Copy the token to your `.env` file

## Pipeline Structure

```yaml
# pipeline.yaml
pipeline:
  - name: Create Jira Notifier
    job: create_notifier
    enabled: true
    params_list: "{{ notifiers }}"
```

```yaml
# inputs.yaml
notifiers:
  - id: "jira-001"
    name: "Jira-Security"
    type: "jira"
    uiEndpoint: "https://acs.example.com"
    labelKey: "notifier.jira"
    labelDefault: "Jira Notifier"
    traits:
      mutabilityMode: "ALLOW_MUTATE"
      visibility: "VISIBLE"
      origin: "IMPERATIVE"
    jira:
      url: "https://jira.example.com"
      username: "acs-service"
      password: "api-token"
      issueType: "Bug"
      priorityMappings:
        - severity: "CRITICAL_SEVERITY"
          priorityName: "Highest"
        - severity: "HIGH_SEVERITY"
          priorityName: "High"
      defaultFieldsJson: '{"project": {"key": "SEC"}}'
      disablePriority: false
```

## Notifier Types

| Type | Config Object | Description |
|------|---------------|-------------|
| `jira` | `JiraConfig` | Jira issue integration |
| `email` | `EmailConfig` | SMTP email notifications |
| `splunk` | `SplunkConfig` | Splunk HEC integration |
| `syslog` | `SyslogConfig` | Syslog (CEF/Legacy) |
| `pagerduty` | `PagerDutyConfig` | PagerDuty incidents |
| `generic` | `GenericConfig` | Generic webhook |
| `cscc` | `CsccConfig` | Google Cloud Security Command Center |
| `sumologic` | `SumologicConfig` | Sumologic HTTP source |
| `awsSecurityHub` | `AwsSecurityHubConfig` | AWS Security Hub |
| `microsoftSentinel` | `MicrosoftSentinelConfig` | Microsoft Sentinel |

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
│       └── notifier/       # Notifier models (split by type)
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
  -v $(pwd)/src/pipelines:/app/pipelines \
  acs-provisioner:latest
```

## Local RHACS Setup (Development)

For local development and API testing:

```bash
# Start Minikube with ACS
make env-up

# Port-forward UI (https://localhost:8443)
make env-ui

# Configure .env for local
API_HOST=localhost
API_PORT=8443
DISABLE_TLS_VERIFY=true

# Run provisioner
make run

# Tear down
make env-down
```
