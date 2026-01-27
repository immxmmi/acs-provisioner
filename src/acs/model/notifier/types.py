"""Notifier type enum."""

from enum import Enum


class NotifierType(str, Enum):
    JIRA = "jira"
    EMAIL = "email"
    CSCC = "cscc"
    SPLUNK = "splunk"
    PAGERDUTY = "pagerduty"
    GENERIC = "generic"
    SUMOLOGIC = "sumologic"
    AWS_SECURITY_HUB = "awsSecurityHub"
    SYSLOG = "syslog"
    MICROSOFT_SENTINEL = "microsoftSentinel"
