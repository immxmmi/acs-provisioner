"""List Notifiers action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListNotifiersAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListNotifiersAction", "Listing all notifiers")
            result = self.gateway.list_notifiers()
            notifiers = result.get("notifiers", [])

            log.info("ListNotifiersAction", f"Found {len(notifiers)} notifiers:")

            # Display each notifier
            for n in notifiers:
                name = n.get("name", "Unknown")
                n_type = n.get("type", "Unknown")
                n_id = n.get("id", "")[:8] + "..." if n.get("id") else ""
                log.info("ListNotifiersAction", f"  - {name} ({n_type}) [{n_id}]")

            return ActionResponse(
                success=True,
                data={"notifiers": notifiers, "count": len(notifiers)}
            )

        except Exception as e:
            log.error("ListNotifiersAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list notifiers: {e}")
