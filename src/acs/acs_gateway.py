"""ACS (Advanced Cluster Security) API Gateway."""

from gateway.client import ApiClient
from utils.logger import Logger as log


class AcsGateway:
    """Gateway for ACS/StackRox API operations."""

    def __init__(self):
        self.client = ApiClient()

    # ==================== AUTH PROVIDERS ====================

    def list_auth_providers(self):
        """List all authentication providers."""
        log.debug("AcsGateway", "Listing auth providers")
        return self.client.get("/v1/authProviders")

    def get_auth_provider(self, provider_id: str):
        """Get a specific auth provider by ID."""
        log.debug("AcsGateway", f"Getting auth provider: {provider_id}")
        return self.client.get(f"/v1/authProviders/{provider_id}")

    def create_auth_provider(self, data: dict):
        """Create a new auth provider."""
        log.debug("AcsGateway", f"Creating auth provider: {data.get('name')}")
        return self.client.post("/v1/authProviders", json=data)

    def update_auth_provider(self, provider_id: str, data: dict):
        """Update an existing auth provider."""
        log.debug("AcsGateway", f"Updating auth provider: {provider_id}")
        return self.client.put(f"/v1/authProviders/{provider_id}", json=data)

    def delete_auth_provider(self, provider_id: str):
        """Delete an auth provider."""
        log.debug("AcsGateway", f"Deleting auth provider: {provider_id}")
        return self.client.delete(f"/v1/authProviders/{provider_id}")

    # ==================== ROLES ====================

    def list_roles(self):
        """List all roles."""
        log.debug("AcsGateway", "Listing roles")
        return self.client.get("/v1/roles")

    def get_role(self, role_name: str):
        """Get a specific role by name."""
        log.debug("AcsGateway", f"Getting role: {role_name}")
        return self.client.get(f"/v1/roles/{role_name}")

    def create_role(self, data: dict):
        """Create a new role."""
        log.debug("AcsGateway", f"Creating role: {data.get('name')}")
        return self.client.post("/v1/roles", json=data)

    def update_role(self, role_name: str, data: dict):
        """Update an existing role."""
        log.debug("AcsGateway", f"Updating role: {role_name}")
        return self.client.put(f"/v1/roles/{role_name}", json=data)

    def delete_role(self, role_name: str):
        """Delete a role."""
        log.debug("AcsGateway", f"Deleting role: {role_name}")
        return self.client.delete(f"/v1/roles/{role_name}")

    # ==================== ACCESS SCOPES ====================

    def list_access_scopes(self):
        """List all access scopes."""
        log.debug("AcsGateway", "Listing access scopes")
        return self.client.get("/v1/simpleaccessscopes")

    def get_access_scope(self, scope_id: str):
        """Get a specific access scope by ID."""
        log.debug("AcsGateway", f"Getting access scope: {scope_id}")
        return self.client.get(f"/v1/simpleaccessscopes/{scope_id}")

    def create_access_scope(self, data: dict):
        """Create a new access scope."""
        log.debug("AcsGateway", f"Creating access scope: {data.get('name')}")
        return self.client.post("/v1/simpleaccessscopes", json=data)

    def update_access_scope(self, scope_id: str, data: dict):
        """Update an existing access scope."""
        log.debug("AcsGateway", f"Updating access scope: {scope_id}")
        return self.client.put(f"/v1/simpleaccessscopes/{scope_id}", json=data)

    def delete_access_scope(self, scope_id: str):
        """Delete an access scope."""
        log.debug("AcsGateway", f"Deleting access scope: {scope_id}")
        return self.client.delete(f"/v1/simpleaccessscopes/{scope_id}")

    # ==================== PERMISSION SETS ====================

    def list_permission_sets(self):
        """List all permission sets."""
        log.debug("AcsGateway", "Listing permission sets")
        return self.client.get("/v1/permissionsets")

    def get_permission_set(self, set_id: str):
        """Get a specific permission set by ID."""
        log.debug("AcsGateway", f"Getting permission set: {set_id}")
        return self.client.get(f"/v1/permissionsets/{set_id}")

    def create_permission_set(self, data: dict):
        """Create a new permission set."""
        log.debug("AcsGateway", f"Creating permission set: {data.get('name')}")
        return self.client.post("/v1/permissionsets", json=data)

    def update_permission_set(self, set_id: str, data: dict):
        """Update an existing permission set."""
        log.debug("AcsGateway", f"Updating permission set: {set_id}")
        return self.client.put(f"/v1/permissionsets/{set_id}", json=data)

    def delete_permission_set(self, set_id: str):
        """Delete a permission set."""
        log.debug("AcsGateway", f"Deleting permission set: {set_id}")
        return self.client.delete(f"/v1/permissionsets/{set_id}")

    # ==================== NOTIFIERS ====================

    def list_notifiers(self):
        """List all notifiers."""
        log.debug("AcsGateway", "Listing notifiers")
        return self.client.get("/v1/notifiers")

    def get_notifier(self, notifier_id: str):
        """Get a specific notifier by ID."""
        log.debug("AcsGateway", f"Getting notifier: {notifier_id}")
        return self.client.get(f"/v1/notifiers/{notifier_id}")

    def create_notifier(self, data: dict):
        """Create a new notifier."""
        log.debug("AcsGateway", f"Creating notifier: {data.get('name')}")
        return self.client.post("/v1/notifiers", json=data)

    def update_notifier(self, notifier_id: str, data: dict):
        """Update an existing notifier."""
        log.debug("AcsGateway", f"Updating notifier: {notifier_id}")
        return self.client.put(f"/v1/notifiers/{notifier_id}", json=data)

    def delete_notifier(self, notifier_id: str):
        """Delete a notifier."""
        log.debug("AcsGateway", f"Deleting notifier: {notifier_id}")
        return self.client.delete(f"/v1/notifiers/{notifier_id}")

    def test_notifier(self, notifier_id: str):
        """Test a notifier configuration."""
        log.debug("AcsGateway", f"Testing notifier: {notifier_id}")
        return self.client.post(f"/v1/notifiers/test/{notifier_id}")

    # ==================== INTEGRATIONS (Image Registries) ====================

    def list_image_integrations(self):
        """List all image integrations."""
        log.debug("AcsGateway", "Listing image integrations")
        return self.client.get("/v1/imageintegrations")

    def get_image_integration(self, integration_id: str):
        """Get a specific image integration by ID."""
        log.debug("AcsGateway", f"Getting image integration: {integration_id}")
        return self.client.get(f"/v1/imageintegrations/{integration_id}")

    def create_image_integration(self, data: dict):
        """Create a new image integration."""
        log.debug("AcsGateway", f"Creating image integration: {data.get('name')}")
        return self.client.post("/v1/imageintegrations", json=data)

    def update_image_integration(self, integration_id: str, data: dict):
        """Update an existing image integration."""
        log.debug("AcsGateway", f"Updating image integration: {integration_id}")
        return self.client.put(f"/v1/imageintegrations/{integration_id}", json=data)

    def delete_image_integration(self, integration_id: str):
        """Delete an image integration."""
        log.debug("AcsGateway", f"Deleting image integration: {integration_id}")
        return self.client.delete(f"/v1/imageintegrations/{integration_id}")

    def test_image_integration(self, data: dict):
        """Test an image integration configuration."""
        log.debug("AcsGateway", "Testing image integration")
        return self.client.post("/v1/imageintegrations/test", json=data)

    # ==================== POLICIES ====================

    def list_policies(self):
        """List all policies."""
        log.debug("AcsGateway", "Listing policies")
        return self.client.get("/v1/policies")

    def get_policy(self, policy_id: str):
        """Get a specific policy by ID."""
        log.debug("AcsGateway", f"Getting policy: {policy_id}")
        return self.client.get(f"/v1/policies/{policy_id}")

    def create_policy(self, data: dict):
        """Create a new policy."""
        log.debug("AcsGateway", f"Creating policy: {data.get('name')}")
        return self.client.post("/v1/policies", json=data)

    def update_policy(self, policy_id: str, data: dict):
        """Update an existing policy."""
        log.debug("AcsGateway", f"Updating policy: {policy_id}")
        return self.client.put(f"/v1/policies/{policy_id}", json=data)

    def delete_policy(self, policy_id: str):
        """Delete a policy."""
        log.debug("AcsGateway", f"Deleting policy: {policy_id}")
        return self.client.delete(f"/v1/policies/{policy_id}")

    def enable_policy(self, policy_id: str):
        """Enable a policy."""
        log.debug("AcsGateway", f"Enabling policy: {policy_id}")
        return self.client.post(f"/v1/policies/{policy_id}/enable")

    def disable_policy(self, policy_id: str):
        """Disable a policy."""
        log.debug("AcsGateway", f"Disabling policy: {policy_id}")
        return self.client.post(f"/v1/policies/{policy_id}/disable")

    # ==================== CLUSTERS ====================

    def list_clusters(self):
        """List all clusters."""
        log.debug("AcsGateway", "Listing clusters")
        return self.client.get("/v1/clusters")

    def get_cluster(self, cluster_id: str):
        """Get a specific cluster by ID."""
        log.debug("AcsGateway", f"Getting cluster: {cluster_id}")
        return self.client.get(f"/v1/clusters/{cluster_id}")
