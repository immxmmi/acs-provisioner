"""Sumologic notifier configuration."""

from typing import Optional
from pydantic import BaseModel


class SumologicConfig(BaseModel):
    http_source_address: Optional[str] = None
    skip_tls_verify: bool = False
