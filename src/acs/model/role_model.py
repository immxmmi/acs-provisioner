"""Pydantic models for ACS Roles."""

from typing import Optional
from pydantic import BaseModel


class Role(BaseModel):
    """ACS Role model."""
    name: str
    description: Optional[str] = None
    permission_set_id: Optional[str] = None
    access_scope_id: Optional[str] = None

    # For linking by name instead of ID
    permission_set_name: Optional[str] = None
    access_scope_name: Optional[str] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
        }

        if self.description:
            payload["description"] = self.description

        if self.permission_set_id:
            payload["permissionSetId"] = self.permission_set_id

        if self.access_scope_id:
            payload["accessScopeId"] = self.access_scope_id

        return payload
