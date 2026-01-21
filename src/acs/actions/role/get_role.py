"""Get Role action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetRoleAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetRoleAction", f"Getting role: {name}")
            role = self.find_by_name(name)

            if role:
                return ActionResponse(success=True, data={"role": role})
            else:
                return ActionResponse(success=False, message=f"Role not found: {name}")

        except Exception as e:
            log.error("GetRoleAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get role: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find role by name."""
        try:
            result = self.gateway.get_role(name)
            return result
        except Exception as e:
            log.debug("GetRoleAction", f"Role not found or error: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if role exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
