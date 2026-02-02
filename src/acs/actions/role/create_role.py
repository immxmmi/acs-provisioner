"""Create Role action."""

from ..base_action import BaseAction
from .get_role import GetRoleAction
from model.action_response import ActionResponse
from acs.model.role_model import Role
from utils.logger import Logger as log


class CreateRoleAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreateRoleAction", "Starting role creation flow")
            role = Role(**data)
            log.debug("CreateRoleAction", f"Resolved model: {role.model_dump()}")

            # Check if already exists
            log.info("CreateRoleAction", f"Checking existence: {role.name}")
            existing = GetRoleAction(gateway=self.gateway).find_by_name(role.name)

            if existing:
                log.info("CreateRoleAction", f"Role already exists, updating: {role.name}")
                merged = {**existing, **data}
                role = Role(**merged)

                if role.permission_set_name and not role.permission_set_id:
                    role.permission_set_id = self._resolve_permission_set(role.permission_set_name)
                if role.access_scope_name and not role.access_scope_id:
                    role.access_scope_id = self._resolve_access_scope(role.access_scope_name)

                payload = role.to_api_payload()
                result = self.gateway.update_role(existing["name"], payload)
                log.info("CreateRoleAction", "Role updated successfully")
                return ActionResponse(success=True, data={"role": role.name, "result": result})

            # Resolve permission set and access scope by name if needed
            if role.permission_set_name and not role.permission_set_id:
                role.permission_set_id = self._resolve_permission_set(role.permission_set_name)

            if role.access_scope_name and not role.access_scope_id:
                role.access_scope_id = self._resolve_access_scope(role.access_scope_name)

            # Create new role
            payload = role.to_api_payload()
            result = self.gateway.create_role(payload)
            log.info("CreateRoleAction", "Role created successfully")

            return ActionResponse(
                success=True,
                data={"role": role.name, "result": result}
            )

        except Exception as e:
            log.error("CreateRoleAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create role: {e}")

    def _resolve_permission_set(self, name: str) -> str:
        """Resolve permission set name to ID."""
        result = self.gateway.list_permission_sets()
        for ps in result.get("permissionSets", []):
            if ps.get("name") == name:
                return ps.get("id")
        raise ValueError(f"Permission set not found: {name}")

    def _resolve_access_scope(self, name: str) -> str:
        """Resolve access scope name to ID."""
        result = self.gateway.list_access_scopes()
        for scope in result.get("accessScopes", []):
            if scope.get("name") == name:
                return scope.get("id")
        raise ValueError(f"Access scope not found: {name}")
