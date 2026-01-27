"""AWS Security Hub notifier configuration."""

from typing import Optional
from pydantic import BaseModel


class AwsSecurityHubCredentials(BaseModel):
    """AWS credentials configuration."""
    accessKeyId: str
    secretAccessKey: str
    stsEnabled: bool


class AwsSecurityHubConfig(BaseModel):
    """AWS Security Hub notifier configuration."""
    region: str
    credentials: AwsSecurityHubCredentials
    accountId: str
