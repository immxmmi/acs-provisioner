"""Common notifier models."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class MutabilityMode(str, Enum):
    """Mutability mode for notifier traits."""
    ALLOW_MUTATE = "ALLOW_MUTATE"
    ALLOW_MUTATE_FORCED = "ALLOW_MUTATE_FORCED"


class Visibility(str, Enum):
    """Visibility for notifier traits."""
    VISIBLE = "VISIBLE"
    HIDDEN = "HIDDEN"


class Origin(str, Enum):
    """Origin for notifier traits."""
    IMPERATIVE = "IMPERATIVE"
    DECLARATIVE = "DECLARATIVE"
    DECLARATIVE_ORPHANED = "DECLARATIVE_ORPHANED"


class NotifierSecret(BaseModel):
    """Notifier secret configuration."""
    secret: Optional[str] = None


class Traits(BaseModel):
    """Notifier traits."""
    mutabilityMode: MutabilityMode
    visibility: Visibility
    origin: Origin
