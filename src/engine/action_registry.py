"""ACS Action Registry - Maps action names to action classes."""

# Auth Provider Actions
from acs.actions.auth_provider.create_auth_provider import CreateAuthProviderAction
from acs.actions.auth_provider.get_auth_provider import GetAuthProviderAction
from acs.actions.auth_provider.list_auth_providers import ListAuthProvidersAction
from acs.actions.auth_provider.delete_auth_provider import DeleteAuthProviderAction
from acs.actions.auth_provider.update_auth_provider import UpdateAuthProviderAction

# Role Actions
from acs.actions.role.create_role import CreateRoleAction
from acs.actions.role.get_role import GetRoleAction
from acs.actions.role.list_roles import ListRolesAction
from acs.actions.role.delete_role import DeleteRoleAction

# Access Scope Actions
from acs.actions.access_scope.create_access_scope import CreateAccessScopeAction
from acs.actions.access_scope.get_access_scope import GetAccessScopeAction
from acs.actions.access_scope.list_access_scopes import ListAccessScopesAction
from acs.actions.access_scope.delete_access_scope import DeleteAccessScopeAction

# Permission Set Actions
from acs.actions.permission_set.create_permission_set import CreatePermissionSetAction
from acs.actions.permission_set.get_permission_set import GetPermissionSetAction
from acs.actions.permission_set.list_permission_sets import ListPermissionSetsAction
from acs.actions.permission_set.delete_permission_set import DeletePermissionSetAction

# Notifier Actions
from acs.actions.notifier.create_notifier import CreateNotifierAction
from acs.actions.notifier.get_notifier import GetNotifierAction
from acs.actions.notifier.list_notifiers import ListNotifiersAction
from acs.actions.notifier.delete_notifier import DeleteNotifierAction
from acs.actions.notifier.test_notifier import TestNotifierAction

# Integration Actions
from acs.actions.integration.create_integration import CreateIntegrationAction
from acs.actions.integration.get_integration import GetIntegrationAction
from acs.actions.integration.list_integrations import ListIntegrationsAction
from acs.actions.integration.delete_integration import DeleteIntegrationAction

# Policy Actions
from acs.actions.policy.create_policy import CreatePolicyAction
from acs.actions.policy.get_policy import GetPolicyAction
from acs.actions.policy.list_policies import ListPoliciesAction
from acs.actions.policy.delete_policy import DeletePolicyAction
from acs.actions.policy.enable_policy import EnablePolicyAction
from acs.actions.policy.disable_policy import DisablePolicyAction


ACTION_REGISTRY = {
    # Auth Provider actions
    "create_auth_provider": CreateAuthProviderAction,
    "get_auth_provider": GetAuthProviderAction,
    "list_auth_providers": ListAuthProvidersAction,
    "delete_auth_provider": DeleteAuthProviderAction,
    "update_auth_provider": UpdateAuthProviderAction,

    # Role actions
    "create_role": CreateRoleAction,
    "get_role": GetRoleAction,
    "list_roles": ListRolesAction,
    "delete_role": DeleteRoleAction,

    # Access Scope actions
    "create_access_scope": CreateAccessScopeAction,
    "get_access_scope": GetAccessScopeAction,
    "list_access_scopes": ListAccessScopesAction,
    "delete_access_scope": DeleteAccessScopeAction,

    # Permission Set actions
    "create_permission_set": CreatePermissionSetAction,
    "get_permission_set": GetPermissionSetAction,
    "list_permission_sets": ListPermissionSetsAction,
    "delete_permission_set": DeletePermissionSetAction,

    # Notifier actions
    "create_notifier": CreateNotifierAction,
    "get_notifier": GetNotifierAction,
    "list_notifiers": ListNotifiersAction,
    "delete_notifier": DeleteNotifierAction,
    "test_notifier": TestNotifierAction,

    # Integration actions (Image Registries)
    "create_integration": CreateIntegrationAction,
    "get_integration": GetIntegrationAction,
    "list_integrations": ListIntegrationsAction,
    "delete_integration": DeleteIntegrationAction,

    # Policy actions
    "create_policy": CreatePolicyAction,
    "get_policy": GetPolicyAction,
    "list_policies": ListPoliciesAction,
    "delete_policy": DeletePolicyAction,
    "enable_policy": EnablePolicyAction,
    "disable_policy": DisablePolicyAction,
}
