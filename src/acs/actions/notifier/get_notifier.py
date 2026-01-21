"""Get Notifier action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetNotifierAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetNotifierAction", f"Getting notifier: {name}")
            notifier = self.find_by_name(name)

            if notifier:
                return ActionResponse(success=True, data={"notifier": notifier})
            else:
                return ActionResponse(success=False, message=f"Notifier not found: {name}")

        except Exception as e:
            log.error("GetNotifierAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get notifier: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find notifier by name."""
        try:
            result = self.gateway.list_notifiers()
            notifiers = result.get("notifiers", [])

            for notifier in notifiers:
                if notifier.get("name") == name:
                    return notifier

            return None
        except Exception as e:
            log.error("GetNotifierAction", f"Error finding notifier: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if notifier exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
