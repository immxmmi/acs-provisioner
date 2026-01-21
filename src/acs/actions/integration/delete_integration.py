"""Delete Image Integration action."""

from ..base_action import BaseAction
from .get_integration import GetIntegrationAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeleteIntegrationAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeleteIntegrationAction", f"Deleting integration: {name}")

            # Find by name to get ID
            integration = GetIntegrationAction(gateway=self.gateway).find_by_name(name)

            if not integration:
                log.info("DeleteIntegrationAction", f"Integration not found: {name}")
                return ActionResponse(success=True, data={"message": f"Integration '{name}' does not exist"})

            integration_id = integration.get("id")
            self.gateway.delete_image_integration(integration_id)
            log.info("DeleteIntegrationAction", f"Integration deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": integration_id})

        except Exception as e:
            log.error("DeleteIntegrationAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete integration: {e}")
