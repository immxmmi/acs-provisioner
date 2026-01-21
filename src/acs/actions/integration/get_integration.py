"""Get Image Integration action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetIntegrationAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetIntegrationAction", f"Getting integration: {name}")
            integration = self.find_by_name(name)

            if integration:
                return ActionResponse(success=True, data={"integration": integration})
            else:
                return ActionResponse(success=False, message=f"Integration not found: {name}")

        except Exception as e:
            log.error("GetIntegrationAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get integration: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find integration by name."""
        try:
            result = self.gateway.list_image_integrations()
            integrations = result.get("integrations", [])

            for integration in integrations:
                if integration.get("name") == name:
                    return integration

            return None
        except Exception as e:
            log.error("GetIntegrationAction", f"Error finding integration: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if integration exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
