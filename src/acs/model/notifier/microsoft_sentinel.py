"""Microsoft Sentinel notifier configuration."""

from pydantic import BaseModel


class DcrConfig(BaseModel):
    """Data Collection Rule configuration."""
    streamName: str
    dataCollectionRuleId: str
    enabled: bool


class ClientCertAuthConfig(BaseModel):
    """Client certificate authentication configuration."""
    clientCert: str
    privateKey: str


class MicrosoftSentinelConfig(BaseModel):
    """Microsoft Sentinel notifier configuration."""
    logIngestionEndpoint: str
    directoryTenantId: str
    applicationClientId: str
    secret: str
    wifEnabled: bool
    alertDcrConfig: DcrConfig
    auditLogDcrConfig: DcrConfig
    clientCertAuthConfig: ClientCertAuthConfig
