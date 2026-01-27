"""Google Cloud Security Command Center notifier configuration."""

from typing import Optional
from pydantic import BaseModel


class CsccConfig(BaseModel):
    service_account: Optional[str] = None
    source_id: Optional[str] = None
    wif_enabled: bool = False
