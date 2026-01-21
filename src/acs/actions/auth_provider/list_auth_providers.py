"""List Auth Providers action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListAuthProvidersAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListAuthProvidersAction", "Listing all auth providers")
            result = self.gateway.list_auth_providers()
            providers = result.get("authProviders", [])

            log.info("ListAuthProvidersAction", f"Found {len(providers)} auth providers")
            return ActionResponse(
                success=True,
                data={"auth_providers": providers, "count": len(providers)}
            )

        except Exception as e:
            log.error("ListAuthProvidersAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list auth providers: {e}")
