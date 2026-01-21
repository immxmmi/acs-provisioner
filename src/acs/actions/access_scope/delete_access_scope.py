"""Delete Access Scope action."""

from ..base_action import BaseAction
from .get_access_scope import GetAccessScopeAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeleteAccessScopeAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeleteAccessScopeAction", f"Deleting access scope: {name}")

            # Find by name to get ID
            scope = GetAccessScopeAction(gateway=self.gateway).find_by_name(name)

            if not scope:
                log.info("DeleteAccessScopeAction", f"Access scope not found: {name}")
                return ActionResponse(success=True, data={"message": f"Access scope '{name}' does not exist"})

            scope_id = scope.get("id")
            self.gateway.delete_access_scope(scope_id)
            log.info("DeleteAccessScopeAction", f"Access scope deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": scope_id})

        except Exception as e:
            log.error("DeleteAccessScopeAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete access scope: {e}")
