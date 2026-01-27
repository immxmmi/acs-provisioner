"""Email notifier configuration."""

from enum import Enum
from pydantic import BaseModel, Field


class StartTLSAuthMethod(str, Enum):
    """StartTLS authentication method."""
    DISABLED = "DISABLED"
    PLAIN = "PLAIN"
    LOGIN = "LOGIN"


class EmailConfig(BaseModel):
    """Email notifier configuration."""
    server: str
    sender: str
    username: str
    password: str
    disableTLS: bool
    DEPRECATEDUseStartTLS: bool
    from_: str = Field(alias="from")
    startTLSAuthMethod: StartTLSAuthMethod
    allowUnauthenticatedSmtp: bool
    skipTLSVerify: bool
    hostnameHeloEhlo: str

    class Config:
        populate_by_name = True
