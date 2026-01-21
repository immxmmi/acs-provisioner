"""Delete Notifier action."""

from ..base_action import BaseAction
from .get_notifier import GetNotifierAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeleteNotifierAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeleteNotifierAction", f"Deleting notifier: {name}")

            # Find by name to get ID
            notifier = GetNotifierAction(gateway=self.gateway).find_by_name(name)

            if not notifier:
                log.info("DeleteNotifierAction", f"Notifier not found: {name}")
                return ActionResponse(success=True, data={"message": f"Notifier '{name}' does not exist"})

            notifier_id = notifier.get("id")
            self.gateway.delete_notifier(notifier_id)
            log.info("DeleteNotifierAction", f"Notifier deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": notifier_id})

        except Exception as e:
            log.error("DeleteNotifierAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete notifier: {e}")
