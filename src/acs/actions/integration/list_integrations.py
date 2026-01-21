"""List Image Integrations action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListIntegrationsAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListIntegrationsAction", "Listing all image integrations")
            result = self.gateway.list_image_integrations()
            integrations = result.get("integrations", [])

            log.info("ListIntegrationsAction", f"Found {len(integrations)} integrations")
            return ActionResponse(
                success=True,
                data={"integrations": integrations, "count": len(integrations)}
            )

        except Exception as e:
            log.error("ListIntegrationsAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list integrations: {e}")
