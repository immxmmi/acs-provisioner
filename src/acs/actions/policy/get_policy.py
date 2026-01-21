"""Get Policy action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetPolicyAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetPolicyAction", f"Getting policy: {name}")
            policy = self.find_by_name(name)

            if policy:
                return ActionResponse(success=True, data={"policy": policy})
            else:
                return ActionResponse(success=False, message=f"Policy not found: {name}")

        except Exception as e:
            log.error("GetPolicyAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get policy: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find policy by name."""
        try:
            result = self.gateway.list_policies()
            policies = result.get("policies", [])

            for policy in policies:
                if policy.get("name") == name:
                    return policy

            return None
        except Exception as e:
            log.error("GetPolicyAction", f"Error finding policy: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if policy exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
