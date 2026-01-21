"""Create Image Integration action."""

from ..base_action import BaseAction
from .get_integration import GetIntegrationAction
from model.action_response import ActionResponse
from acs.model.integration_model import ImageIntegration
from utils.logger import Logger as log


class CreateIntegrationAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreateIntegrationAction", "Starting image integration creation flow")
            integration = ImageIntegration(**data)
            log.debug("CreateIntegrationAction", f"Resolved model: {integration.model_dump()}")

            # Check if already exists
            log.info("CreateIntegrationAction", f"Checking existence: {integration.name}")
            existing = GetIntegrationAction(gateway=self.gateway).find_by_name(integration.name)

            if existing:
                log.info("CreateIntegrationAction", f"Integration already exists: {integration.name}")
                return ActionResponse(success=True, data={"integration": integration.name, "id": existing.get("id")})

            # Create new integration
            payload = integration.to_api_payload()
            result = self.gateway.create_image_integration(payload)
            log.info("CreateIntegrationAction", "Integration created successfully")

            return ActionResponse(
                success=True,
                data={"integration": integration.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreateIntegrationAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create integration: {e}")
