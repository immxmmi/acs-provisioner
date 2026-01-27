"""Splunk notifier configuration."""

from typing import Dict
from pydantic import BaseModel


class SourceType(BaseModel):
    """Splunk source type configuration."""

    class Config:
        extra = "allow"


class SplunkConfig(BaseModel):
    """Splunk notifier configuration."""
    httpToken: str
    httpEndpoint: str
    insecure: bool
    truncate: int
    auditLoggingEnabled: bool
    derivedSourceType: bool
    sourceType: Dict[str, str]
