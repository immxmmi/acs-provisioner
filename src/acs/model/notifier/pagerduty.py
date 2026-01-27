"""PagerDuty notifier configuration."""

from pydantic import BaseModel


class PagerDutyConfig(BaseModel):
    api_key: str
