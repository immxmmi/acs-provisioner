"""Create Notifier action."""

from ..base_action import BaseAction
from .get_notifier import GetNotifierAction
from model.action_response import ActionResponse
from acs.model.notifier_model import Notifier
from utils.logger import Logger as log


class CreateNotifierAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreateNotifierAction", "Starting notifier creation flow")
            notifier = Notifier(**data)
            log.debug("CreateNotifierAction", f"Resolved model: {notifier.model_dump()}")

            # Check if already exists
            log.info("CreateNotifierAction", f"Checking existence: {notifier.name}")
            existing = GetNotifierAction(gateway=self.gateway).find_by_name(notifier.name)

            if existing:
                log.info("CreateNotifierAction", f"Notifier already exists: {notifier.name}")
                return ActionResponse(success=True, data={"notifier": notifier.name, "id": existing.get("id")})

            # Create new notifier
            payload = notifier.to_api_payload()
            result = self.gateway.create_notifier(payload)
            log.info("CreateNotifierAction", "Notifier created successfully")

            return ActionResponse(
                success=True,
                data={"notifier": notifier.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreateNotifierAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create notifier: {e}")
