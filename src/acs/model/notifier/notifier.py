"""Main Notifier model."""

from typing import Optional
from pydantic import BaseModel

from .types import NotifierType
from .jira import JiraConfig
from .email import EmailConfig
from .splunk import SplunkConfig
from .pagerduty import PagerDutyConfig
from .generic import GenericConfig
from .cscc import CsccConfig
from .sumologic import SumologicConfig
from .aws_security_hub import AwsSecurityHubConfig
from .syslog import SyslogConfig
from .microsoft_sentinel import MicrosoftSentinelConfig
from .common import Traits


class Notifier(BaseModel):
    """ACS Notifier model.

    All fields optional to support both:
    - Create: provide the fields you need
    - GET/List: no fields needed, response comes from server
    """
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[NotifierType] = None
    uiEndpoint: Optional[str] = None
    labelKey: Optional[str] = None
    labelDefault: Optional[str] = None

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
    notifierSecret: Optional[str] = None
    traits: Optional[Traits] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {}

        if self.id:
            payload["id"] = self.id
        if self.name:
            payload["name"] = self.name
        if self.type:
            payload["type"] = self.type.value
        if self.uiEndpoint:
            payload["uiEndpoint"] = self.uiEndpoint
        if self.labelKey:
            payload["labelKey"] = self.labelKey
        if self.labelDefault:
            payload["labelDefault"] = self.labelDefault

        # Add traits if present
        if self.traits:
            payload["traits"] = {
                "mutabilityMode": self.traits.mutabilityMode.value,
                "visibility": self.traits.visibility.value,
                "origin": self.traits.origin.value,
            }

        # Add notifierSecret if present
        if self.notifierSecret:
            payload["notifierSecret"] = self.notifierSecret

        # Type-specific payloads
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
                "apiKey": self.pagerduty.apiKey,
            }

        elif self.type == NotifierType.GENERIC and self.generic:
            payload["generic"] = {
                "endpoint": self.generic.endpoint,
                "skipTLSVerify": self.generic.skipTLSVerify,
                "auditLoggingEnabled": self.generic.auditLoggingEnabled,
            }
            if self.generic.caCert:
                payload["generic"]["caCert"] = self.generic.caCert
            if self.generic.username:
                payload["generic"]["username"] = self.generic.username
            if self.generic.password:
                payload["generic"]["password"] = self.generic.password
            if self.generic.headers:
                payload["generic"]["headers"] = self.generic.headers
            if self.generic.extraFields:
                payload["generic"]["extraFields"] = self.generic.extraFields

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

        elif self.type == NotifierType.SYSLOG and self.syslog:
            payload["syslog"] = {
                "localFacility": self.syslog.localFacility.value,
                "messageFormat": self.syslog.messageFormat.value,
                "maxMessageSize": self.syslog.maxMessageSize,
            }
            if self.syslog.tcpConfig:
                payload["syslog"]["tcpConfig"] = self.syslog.tcpConfig
            if self.syslog.extraFields:
                payload["syslog"]["extraFields"] = self.syslog.extraFields

        elif self.type == NotifierType.CSCC and self.cscc:
            payload["cscc"] = {
                "serviceAccount": self.cscc.serviceAccount,
                "sourceId": self.cscc.sourceId,
                "wifEnabled": self.cscc.wifEnabled,
            }

        elif self.type == NotifierType.SUMOLOGIC and self.sumologic:
            payload["sumologic"] = {
                "httpSourceAddress": self.sumologic.httpSourceAddress,
                "skipTLSVerify": self.sumologic.skipTLSVerify,
            }

        elif self.type == NotifierType.AWS_SECURITY_HUB and self.awsSecurityHub:
            payload["awsSecurityHub"] = {
                "region": self.awsSecurityHub.region,
                "accountId": self.awsSecurityHub.accountId,
                "credentials": {
                    "accessKeyId": self.awsSecurityHub.credentials.accessKeyId,
                    "secretAccessKey": self.awsSecurityHub.credentials.secretAccessKey,
                    "stsEnabled": self.awsSecurityHub.credentials.stsEnabled,
                },
            }

        elif self.type == NotifierType.MICROSOFT_SENTINEL and self.microsoftSentinel:
            payload["microsoftSentinel"] = {
                "logIngestionEndpoint": self.microsoftSentinel.logIngestionEndpoint,
                "directoryTenantId": self.microsoftSentinel.directoryTenantId,
                "applicationClientId": self.microsoftSentinel.applicationClientId,
                "secret": self.microsoftSentinel.secret,
                "wifEnabled": self.microsoftSentinel.wifEnabled,
                "alertDcrConfig": {
                    "streamName": self.microsoftSentinel.alertDcrConfig.streamName,
                    "dataCollectionRuleId": self.microsoftSentinel.alertDcrConfig.dataCollectionRuleId,
                    "enabled": self.microsoftSentinel.alertDcrConfig.enabled,
                },
                "auditLogDcrConfig": {
                    "streamName": self.microsoftSentinel.auditLogDcrConfig.streamName,
                    "dataCollectionRuleId": self.microsoftSentinel.auditLogDcrConfig.dataCollectionRuleId,
                    "enabled": self.microsoftSentinel.auditLogDcrConfig.enabled,
                },
                "clientCertAuthConfig": {
                    "clientCert": self.microsoftSentinel.clientCertAuthConfig.clientCert,
                    "privateKey": self.microsoftSentinel.clientCertAuthConfig.privateKey,
                },
            }

        return payload
