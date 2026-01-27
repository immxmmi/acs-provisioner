"""Main Notifier model."""

from typing import Optional
from pydantic import BaseModel

from .types import NotifierType
from .jira import JiraConfig
from .email import EmailConfig
from .splunk import SplunkConfig
from .pagerduty import PagerDutyConfig
from .generic import GenericConfig, WebhookConfig
from .cscc import CsccConfig
from .sumologic import SumologicConfig
from .aws_security_hub import AwsSecurityHubConfig
from .syslog import SyslogConfig
from .microsoft_sentinel import MicrosoftSentinelConfig
from .common import NotifierSecret, Traits


class Notifier(BaseModel):
    """ACS Notifier model."""
    # Required fields
    id: str
    name: str
    type: NotifierType
    uiEndpoint: str
    labelKey: str
    labelDefault: str

    # Type-specific configs (optional)
    jira: Optional[JiraConfig] = None
    email: Optional[EmailConfig] = None
    cscc: Optional[CsccConfig] = None
    splunk: Optional[SplunkConfig] = None
    pagerduty: Optional[PagerDutyConfig] = None
    generic: Optional[GenericConfig] = None
    sumologic: Optional[SumologicConfig] = None
    awsSecurityHub: Optional[AwsSecurityHubConfig] = None
    syslog: Optional[SyslogConfig] = None
    microsoftSentinel: Optional[MicrosoftSentinelConfig] = None
    notifierSecret: Optional[NotifierSecret] = None
    traits: Optional[Traits] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
            "type": self.type.value,
            "id": self.id,
            "uiEndpoint": self.uiEndpoint,
            "labelKey": self.labelKey,
            "labelDefault": self.labelDefault,
        }

        if self.type == NotifierType.EMAIL and self.email:
            payload["email"] = {
                "server": self.email.server,
                "sender": self.email.sender,
                "username": self.email.username,
                "password": self.email.password,
                "disableTLS": self.email.disableTLS,
                "DEPRECATEDUseStartTLS": self.email.DEPRECATEDUseStartTLS,
                "from": self.email.from_,
                "startTLSAuthMethod": self.email.startTLSAuthMethod.value,
                "allowUnauthenticatedSmtp": self.email.allowUnauthenticatedSmtp,
                "skipTLSVerify": self.email.skipTLSVerify,
                "hostnameHeloEhlo": self.email.hostnameHeloEhlo,
            }

        elif self.type == NotifierType.JIRA and self.jira:
            payload["jira"] = {
                "url": self.jira.url,
                "username": self.jira.username,
                "password": self.jira.password,
                "issueType": self.jira.issueType,
                "priorityMappings": [
                    {"severity": m.severity, "priorityName": m.priorityName}
                    for m in self.jira.priorityMappings
                ],
                "defaultFieldsJson": self.jira.defaultFieldsJson,
                "disablePriority": self.jira.disablePriority,
            }

        elif self.type == NotifierType.PAGERDUTY and self.pagerduty:
            payload["pagerduty"] = {
                "apiKey": self.pagerduty.api_key,
            }

        elif self.type == NotifierType.GENERIC and self.generic:
            payload["generic"] = {
                "endpoint": self.generic.endpoint,
                "skipTLSVerify": self.generic.skip_tls_verify,
            }
            if self.generic.headers:
                payload["generic"]["headers"] = self.generic.headers

        elif self.type == NotifierType.SPLUNK and self.splunk:
            payload["splunk"] = {
                "httpToken": self.splunk.httpToken,
                "httpEndpoint": self.splunk.httpEndpoint,
                "insecure": self.splunk.insecure,
                "truncate": self.splunk.truncate,
                "auditLoggingEnabled": self.splunk.auditLoggingEnabled,
                "derivedSourceType": self.splunk.derivedSourceType,
                "sourceType": self.splunk.sourceType,
            }

        return payload
