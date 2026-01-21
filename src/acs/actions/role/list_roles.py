"""List Roles action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListRolesAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListRolesAction", "Listing all roles")
            result = self.gateway.list_roles()
            roles = result.get("roles", [])

            log.info("ListRolesAction", f"Found {len(roles)} roles")
            return ActionResponse(
                success=True,
                data={"roles": roles, "count": len(roles)}
            )

        except Exception as e:
            log.error("ListRolesAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list roles: {e}")
