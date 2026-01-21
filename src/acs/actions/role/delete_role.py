"""Delete Role action."""

from ..base_action import BaseAction
from .get_role import GetRoleAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeleteRoleAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeleteRoleAction", f"Deleting role: {name}")

            # Check if exists
            if not GetRoleAction.exists(self.gateway, name):
                log.info("DeleteRoleAction", f"Role not found: {name}")
                return ActionResponse(success=True, data={"message": f"Role '{name}' does not exist"})

            self.gateway.delete_role(name)
            log.info("DeleteRoleAction", f"Role deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name})

        except Exception as e:
            log.error("DeleteRoleAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete role: {e}")
