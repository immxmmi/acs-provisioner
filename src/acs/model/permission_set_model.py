"""Pydantic models for ACS Permission Sets."""

from typing import Optional, Dict
from pydantic import BaseModel


class PermissionSet(BaseModel):
    """ACS Permission Set model."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None

    # Resource to access level mapping
    # Access levels: NO_ACCESS, READ_ACCESS, READ_WRITE_ACCESS
    resource_to_access: Optional[Dict[str, str]] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
        }

        if self.id:
            payload["id"] = self.id

        if self.description:
            payload["description"] = self.description

        if self.resource_to_access:
            payload["resourceToAccess"] = self.resource_to_access

        return payload


# Available resources in ACS for permission sets
ACS_RESOURCES = [
    "Access",
    "Administration",
    "Alert",
    "CVE",
    "Cluster",
    "Compliance",
    "Deployment",
    "DeploymentExtension",
    "Detection",
    "Image",
    "Integration",
    "K8sRole",
    "K8sRoleBinding",
    "K8sSubject",
    "Namespace",
    "NetworkGraph",
    "NetworkPolicy",
    "Node",
    "Policy",
    "Role",
    "Secret",
    "ServiceAccount",
    "VulnerabilityManagementApprovals",
    "VulnerabilityManagementRequests",
    "WatchedImage",
    "WorkflowAdministration",
]

ACCESS_LEVELS = [
    "NO_ACCESS",
    "READ_ACCESS",
    "READ_WRITE_ACCESS",
]
