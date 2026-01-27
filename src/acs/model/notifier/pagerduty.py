"""PagerDuty notifier configuration."""

from pydantic import BaseModel


class PagerDutyConfig(BaseModel):
    """PagerDuty notifier configuration."""
    apiKey: str
