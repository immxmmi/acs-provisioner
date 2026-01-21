"""List Access Scopes action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListAccessScopesAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListAccessScopesAction", "Listing all access scopes")
            result = self.gateway.list_access_scopes()
            scopes = result.get("accessScopes", [])

            log.info("ListAccessScopesAction", f"Found {len(scopes)} access scopes")
            return ActionResponse(
                success=True,
                data={"access_scopes": scopes, "count": len(scopes)}
            )

        except Exception as e:
            log.error("ListAccessScopesAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list access scopes: {e}")
