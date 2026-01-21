"""Pydantic models for ACS Policies."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class PolicySection(BaseModel):
    """Policy section with criteria groups."""
    section_name: Optional[str] = None
    policy_groups: List[Dict[str, Any]]


class Exclusion(BaseModel):
    """Policy exclusion definition."""
    name: str
    deployment: Optional[Dict[str, Any]] = None
    image: Optional[Dict[str, Any]] = None
    expiration: Optional[str] = None


class Scope(BaseModel):
    """Policy scope definition."""
    cluster: Optional[str] = None
    namespace: Optional[str] = None
    label: Optional[Dict[str, str]] = None


class Policy(BaseModel):
    """ACS Security Policy model."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None

    # Severity: LOW_SEVERITY, MEDIUM_SEVERITY, HIGH_SEVERITY, CRITICAL_SEVERITY
    severity: str = "MEDIUM_SEVERITY"

    # Categories
    categories: List[str] = []

    # Lifecycle stages: DEPLOY, BUILD, RUNTIME
    lifecycle_stages: List[str] = ["DEPLOY"]

    # Event source for runtime: NOT_APPLICABLE, DEPLOYMENT_EVENT, AUDIT_LOG_EVENT
    event_source: str = "NOT_APPLICABLE"

    # Enforcement actions
    enforcement_actions: List[str] = []  # UNSET_ENFORCEMENT, SCALE_TO_ZERO_ENFORCEMENT, FAIL_BUILD_ENFORCEMENT, etc.

    # Policy sections with criteria
    policy_sections: Optional[List[PolicySection]] = None

    # Exclusions
    exclusions: Optional[List[Exclusion]] = None

    # Scope restrictions
    scope: Optional[List[Scope]] = None

    # Disabled flag
    disabled: bool = False

    # Remediation
    remediation: Optional[str] = None

    # Rationale
    rationale: Optional[str] = None

    # MITRE ATT&CK
    mitre_attack_vectors: Optional[List[Dict[str, Any]]] = None

    # Is default policy
    is_default: bool = False

    # Criteria lock
    criteria_locked: bool = False
    mitre_vectors_locked: bool = False

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
            "severity": self.severity,
            "categories": self.categories,
            "lifecycleStages": self.lifecycle_stages,
            "eventSource": self.event_source,
            "disabled": self.disabled,
            "isDefault": self.is_default,
            "criteriaLocked": self.criteria_locked,
            "mitreVectorsLocked": self.mitre_vectors_locked,
        }

        if self.id:
            payload["id"] = self.id

        if self.description:
            payload["description"] = self.description

        if self.enforcement_actions:
            payload["enforcementActions"] = self.enforcement_actions

        if self.policy_sections:
            payload["policySections"] = [
                {
                    "sectionName": s.section_name or "",
                    "policyGroups": s.policy_groups,
                }
                for s in self.policy_sections
            ]

        if self.exclusions:
            payload["exclusions"] = [
                {
                    "name": e.name,
                    "deployment": e.deployment or {},
                    "image": e.image or {},
                    "expiration": e.expiration,
                }
                for e in self.exclusions
            ]

        if self.scope:
            payload["scope"] = [
                {
                    "cluster": s.cluster,
                    "namespace": s.namespace,
                    "label": s.label,
                }
                for s in self.scope
            ]

        if self.remediation:
            payload["remediation"] = self.remediation

        if self.rationale:
            payload["rationale"] = self.rationale

        if self.mitre_attack_vectors:
            payload["mitreAttackVectors"] = self.mitre_attack_vectors

        return payload


# Common policy categories in ACS
POLICY_CATEGORIES = [
    "Anomalous Activity",
    "Cryptocurrency Mining",
    "DevOps Best Practices",
    "Kubernetes",
    "Network Tools",
    "Package Management",
    "Privileges",
    "Security Best Practices",
    "System Modification",
    "Vulnerability Management",
]

# Severity levels
SEVERITY_LEVELS = [
    "LOW_SEVERITY",
    "MEDIUM_SEVERITY",
    "HIGH_SEVERITY",
    "CRITICAL_SEVERITY",
]
