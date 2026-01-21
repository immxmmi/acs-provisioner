"""Get Access Scope action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetAccessScopeAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetAccessScopeAction", f"Getting access scope: {name}")
            scope = self.find_by_name(name)

            if scope:
                return ActionResponse(success=True, data={"access_scope": scope})
            else:
                return ActionResponse(success=False, message=f"Access scope not found: {name}")

        except Exception as e:
            log.error("GetAccessScopeAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get access scope: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find access scope by name."""
        try:
            result = self.gateway.list_access_scopes()
            scopes = result.get("accessScopes", [])

            for scope in scopes:
                if scope.get("name") == name:
                    return scope

            return None
        except Exception as e:
            log.error("GetAccessScopeAction", f"Error finding access scope: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if access scope exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
