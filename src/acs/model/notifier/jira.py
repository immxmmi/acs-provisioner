"""Jira notifier configuration."""

from typing import List
from pydantic import BaseModel


class JiraPriorityMapping(BaseModel):
    """Jira priority mapping for severity levels."""
    severity: str  # e.g. "UNSET_SEVERITY", "LOW_SEVERITY", "MEDIUM_SEVERITY", "HIGH_SEVERITY", "CRITICAL_SEVERITY"
    priorityName: str


class JiraConfig(BaseModel):
    """Jira notifier configuration."""
    url: str
    username: str
    password: str
    issueType: str
    priorityMappings: List[JiraPriorityMapping]
    defaultFieldsJson: str
    disablePriority: bool
