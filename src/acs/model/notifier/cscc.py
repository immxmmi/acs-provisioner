"""Google Cloud Security Command Center notifier configuration."""

from pydantic import BaseModel


class CsccConfig(BaseModel):
    """Google Cloud Security Command Center configuration."""
    serviceAccount: str
    sourceId: str
    wifEnabled: bool
