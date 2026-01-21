"""Delete Permission Set action."""

from ..base_action import BaseAction
from .get_permission_set import GetPermissionSetAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeletePermissionSetAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeletePermissionSetAction", f"Deleting permission set: {name}")

            # Find by name to get ID
            perm_set = GetPermissionSetAction(gateway=self.gateway).find_by_name(name)

            if not perm_set:
                log.info("DeletePermissionSetAction", f"Permission set not found: {name}")
                return ActionResponse(success=True, data={"message": f"Permission set '{name}' does not exist"})

            set_id = perm_set.get("id")
            self.gateway.delete_permission_set(set_id)
            log.info("DeletePermissionSetAction", f"Permission set deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": set_id})

        except Exception as e:
            log.error("DeletePermissionSetAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete permission set: {e}")
