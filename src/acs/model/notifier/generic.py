"""Generic webhook notifier configuration."""

from typing import Optional, List
from pydantic import BaseModel


class GenericConfig(BaseModel):
    endpoint: Optional[str] = None
    skip_tls_verify: bool = False
    ca_cert: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    headers: Optional[List[dict]] = None
    extra_fields: Optional[List[dict]] = None
    audit_logging_enabled: bool = False


class WebhookConfig(BaseModel):
    """Legacy webhook notifier configuration."""
    endpoint: str
    skip_tls_verify: bool = False
    headers: Optional[List[dict]] = None
