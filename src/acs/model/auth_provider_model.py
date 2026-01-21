"""Pydantic models for ACS Auth Providers."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class OidcConfig(BaseModel):
    """OIDC configuration for auth provider."""
    issuer: str
    client_id: str
    client_secret: Optional[str] = None
    mode: str = "auto"  # auto, post, query, fragment
    disable_offline_access_scope: bool = False


class SamlConfig(BaseModel):
    """SAML configuration for auth provider."""
    sp_issuer: str
    idp_metadata_url: Optional[str] = None
    idp_issuer: Optional[str] = None
    idp_sso_url: Optional[str] = None
    idp_cert_pem: Optional[str] = None


class LdapConfig(BaseModel):
    """LDAP configuration for auth provider."""
    host: str
    port: int = 389
    base_dn: str
    bind_dn: Optional[str] = None
    bind_password: Optional[str] = None
    use_starttls: bool = False


class GroupMapping(BaseModel):
    """Group to role mapping."""
    key: str
    value: str
    role: str


class AuthProvider(BaseModel):
    """ACS Auth Provider model."""
    id: Optional[str] = None
    name: str
    type: str  # oidc, saml, ldap, userpki, iap
    enabled: bool = True

    # Type-specific configs
    oidc: Optional[OidcConfig] = None
    saml: Optional[SamlConfig] = None
    ldap: Optional[LdapConfig] = None

    # UI endpoint (for redirects)
    ui_endpoint: Optional[str] = None

    # Required attributes for access
    required_attributes: Optional[List[Dict[str, str]]] = None

    # Group mappings
    groups: Optional[List[GroupMapping]] = None

    # Default role if no group matches
    default_role: Optional[str] = None

    class Config:
        extra = "allow"

    def to_api_payload(self) -> dict:
        """Convert to ACS API payload format."""
        payload = {
            "name": self.name,
            "type": self.type,
            "enabled": self.enabled,
        }

        if self.id:
            payload["id"] = self.id

        if self.ui_endpoint:
            payload["uiEndpoint"] = self.ui_endpoint

        if self.type == "oidc" and self.oidc:
            payload["config"] = {
                "issuer": self.oidc.issuer,
                "client_id": self.oidc.client_id,
                "mode": self.oidc.mode,
                "disable_offline_access_scope": self.oidc.disable_offline_access_scope,
            }
            if self.oidc.client_secret:
                payload["config"]["client_secret"] = self.oidc.client_secret

        elif self.type == "saml" and self.saml:
            payload["config"] = {
                "sp_issuer": self.saml.sp_issuer,
            }
            if self.saml.idp_metadata_url:
                payload["config"]["idp_metadata_url"] = self.saml.idp_metadata_url
            if self.saml.idp_issuer:
                payload["config"]["idp_issuer"] = self.saml.idp_issuer
            if self.saml.idp_sso_url:
                payload["config"]["idp_sso_url"] = self.saml.idp_sso_url
            if self.saml.idp_cert_pem:
                payload["config"]["idp_cert_pem"] = self.saml.idp_cert_pem

        if self.required_attributes:
            payload["requiredAttributes"] = self.required_attributes

        return payload
