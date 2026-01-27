"""Syslog notifier configuration."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class LocalFacility(str, Enum):
    """Syslog local facility."""
    LOCAL0 = "LOCAL0"
    LOCAL1 = "LOCAL1"
    LOCAL2 = "LOCAL2"
    LOCAL3 = "LOCAL3"
    LOCAL4 = "LOCAL4"
    LOCAL5 = "LOCAL5"
    LOCAL6 = "LOCAL6"
    LOCAL7 = "LOCAL7"


class MessageFormat(str, Enum):
    """Syslog message format."""
    LEGACY = "LEGACY"
    CEF = "CEF"


class SyslogConfig(BaseModel):
    """Syslog notifier configuration."""
    localFacility: LocalFacility
    messageFormat: MessageFormat
    maxMessageSize: int
    tcpConfig: Optional[dict] = None
    extraFields: Optional[List[dict]] = None
