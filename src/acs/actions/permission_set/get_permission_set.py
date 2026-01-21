"""Get Permission Set action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetPermissionSetAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetPermissionSetAction", f"Getting permission set: {name}")
            perm_set = self.find_by_name(name)

            if perm_set:
                return ActionResponse(success=True, data={"permission_set": perm_set})
            else:
                return ActionResponse(success=False, message=f"Permission set not found: {name}")

        except Exception as e:
            log.error("GetPermissionSetAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get permission set: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find permission set by name."""
        try:
            result = self.gateway.list_permission_sets()
            perm_sets = result.get("permissionSets", [])

            for ps in perm_sets:
                if ps.get("name") == name:
                    return ps

            return None
        except Exception as e:
            log.error("GetPermissionSetAction", f"Error finding permission set: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if permission set exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
