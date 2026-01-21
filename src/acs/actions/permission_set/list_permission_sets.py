"""List Permission Sets action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListPermissionSetsAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListPermissionSetsAction", "Listing all permission sets")
            result = self.gateway.list_permission_sets()
            perm_sets = result.get("permissionSets", [])

            log.info("ListPermissionSetsAction", f"Found {len(perm_sets)} permission sets")
            return ActionResponse(
                success=True,
                data={"permission_sets": perm_sets, "count": len(perm_sets)}
            )

        except Exception as e:
            log.error("ListPermissionSetsAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list permission sets: {e}")
