"""Sumologic notifier configuration."""

from pydantic import BaseModel


class SumologicConfig(BaseModel):
    """Sumologic notifier configuration."""
    httpSourceAddress: str
    skipTLSVerify: bool
