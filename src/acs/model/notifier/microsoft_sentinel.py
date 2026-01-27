"""Microsoft Sentinel notifier configuration."""

from typing import Optional
from pydantic import BaseModel


class MicrosoftSentinelConfig(BaseModel):
    """Microsoft Sentinel notifier configuration."""
    log_ingestion_endpoint: Optional[str] = None
    directory_tenant_id: Optional[str] = None
    application_client_id: Optional[str] = None
    secret: Optional[str] = None
    alert_dcr_rule_id: Optional[str] = None
    alert_dcr_stream_name: Optional[str] = None
