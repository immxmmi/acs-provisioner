"""Generic webhook notifier configuration."""

from typing import Optional, List
from pydantic import BaseModel


class GenericConfig(BaseModel):
    """Generic webhook notifier configuration."""
    endpoint: str
    skipTLSVerify: bool
    caCert: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    headers: Optional[List[dict]] = None
    extraFields: Optional[List[dict]] = None
    auditLoggingEnabled: bool
