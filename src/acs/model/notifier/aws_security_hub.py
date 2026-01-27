"""AWS Security Hub notifier configuration."""

from typing import Optional
from pydantic import BaseModel


class AwsSecurityHubConfig(BaseModel):
    region: Optional[str] = None
    credentials: Optional[dict] = None
    account_id: Optional[str] = None
