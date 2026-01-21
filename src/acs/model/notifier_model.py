"""Pydantic models for ACS Notifiers."""

from typing import Optional, List
from pydantic import BaseModel


class SlackConfig(BaseModel):
    """Slack notifier configuration."""
    webhook: str
    channel: Optional[str] = None


class EmailConfig(BaseModel):
    """Email notifier configuration."""
    server: str
    port: int = 587
    sender: str
    username: Optional[str] = None
    password: Optional[str] = None
    use_starttls: bool = True
    disable_tls: bool = False
    default_recipient: Optional[str] = None


class JiraConfig(BaseModel):
    """Jira notifier configuration."""
    url: str
    username: str
    password: str  # API token
    project: str
    issue_type: str = "Task"


class PagerDutyConfig(BaseModel):
    """PagerDuty notifier configuration."""
    api_key: str


class WebhookConfig(BaseModel):
    """Generic webhook notifier configuration."""
    endpoint: str
    skip_tls_verify: bool = False
    headers: Optional[List[dict]] = None


class SplunkConfig(BaseModel):
    """Splunk notifier configuration."""
    http_endpoint: str
    http_token: str
    source_type: Optional[str] = None
    truncate: int = 10000


class Notifier(BaseModel):
    """ACS Notifier model."""
    id: Optional[str] = None
    name: str
    type: str  # slack, email, jira, pagerduty, generic, splunk, teams, syslog, cscc

    # Type-specific configs
    slack: Optional[SlackConfig] = None
    email: Optional[EmailConfig] = None
    jira: Optional[JiraConfig] = None
    pagerduty: Optional[PagerDutyConfig] = None
    webhook: Optional[WebhookConfig] = None
    splunk: Optional[SplunkConfig] = None

    # UI endpoint
    ui_endpoint: Optional[str] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
            "type": self.type,
        }

        if self.id:
            payload["id"] = self.id

        if self.ui_endpoint:
            payload["uiEndpoint"] = self.ui_endpoint

        if self.type == "slack" and self.slack:
            payload["slack"] = {
                "webhook": self.slack.webhook,
            }
            if self.slack.channel:
                payload["slack"]["channel"] = self.slack.channel

        elif self.type == "email" and self.email:
            payload["email"] = {
                "server": self.email.server,
                "port": self.email.port,
                "sender": self.email.sender,
                "startTLSAuthMethod": "PLAIN" if self.email.use_starttls else "DISABLED",
                "disableTLS": self.email.disable_tls,
            }
            if self.email.username:
                payload["email"]["username"] = self.email.username
            if self.email.password:
                payload["email"]["password"] = self.email.password
            if self.email.default_recipient:
                payload["email"]["DEFAULTRecipient"] = self.email.default_recipient

        elif self.type == "jira" and self.jira:
            payload["jira"] = {
                "url": self.jira.url,
                "username": self.jira.username,
                "password": self.jira.password,
                "issueType": self.jira.issue_type,
                "defaultFieldsJson": f'{{"project": {{"key": "{self.jira.project}"}}}}',
            }

        elif self.type == "pagerduty" and self.pagerduty:
            payload["pagerduty"] = {
                "apiKey": self.pagerduty.api_key,
            }

        elif self.type == "generic" and self.webhook:
            payload["generic"] = {
                "endpoint": self.webhook.endpoint,
                "skipTLSVerify": self.webhook.skip_tls_verify,
            }
            if self.webhook.headers:
                payload["generic"]["headers"] = self.webhook.headers

        elif self.type == "splunk" and self.splunk:
            payload["splunk"] = {
                "httpEndpoint": self.splunk.http_endpoint,
                "httpToken": self.splunk.http_token,
                "truncate": self.splunk.truncate,
            }
            if self.splunk.source_type:
                payload["splunk"]["sourceType"] = self.splunk.source_type

        return payload
