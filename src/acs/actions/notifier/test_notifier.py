"""Test Notifier action."""

from ..base_action import BaseAction
from .get_notifier import GetNotifierAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class TestNotifierAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("TestNotifierAction", f"Testing notifier: {name}")

            # Find by name to get ID
            notifier = GetNotifierAction(gateway=self.gateway).find_by_name(name)

            if not notifier:
                return ActionResponse(success=False, message=f"Notifier not found: {name}")

            notifier_id = notifier.get("id")
            result = self.gateway.test_notifier(notifier_id)
            log.info("TestNotifierAction", f"Notifier test completed: {name}")

            return ActionResponse(success=True, data={"tested": name, "result": result})

        except Exception as e:
            log.error("TestNotifierAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to test notifier: {e}")
