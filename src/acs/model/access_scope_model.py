"""Pydantic models for ACS Access Scopes."""

from typing import Optional, List, Dict
from pydantic import BaseModel


class ClusterScope(BaseModel):
    """Cluster-level scope definition."""
    cluster: str
    namespaces: Optional[List[str]] = None


class LabelSelector(BaseModel):
    """Label selector for scope rules."""
    requirements: List[Dict[str, any]]


class AccessScope(BaseModel):
    """ACS Access Scope model (SimpleAccessScope)."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None

    # Simple rules - list of cluster/namespace combinations
    rules: Optional[List[ClusterScope]] = None

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

        if self.rules:
            payload["rules"] = {
                "includedClusters": [],
                "includedNamespaces": [],
                "clusterLabelSelectors": [],
                "namespaceLabelSelectors": [],
            }

            for rule in self.rules:
                if rule.namespaces:
                    for ns in rule.namespaces:
                        payload["rules"]["includedNamespaces"].append({
                            "clusterName": rule.cluster,
                            "namespaceName": ns,
                        })
                else:
                    payload["rules"]["includedClusters"].append(rule.cluster)

        return payload
