"""Get Auth Provider action."""

from typing import Optional
from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class GetAuthProviderAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("GetAuthProviderAction", f"Getting auth provider: {name}")
            provider = self.find_by_name(name)

            if provider:
                return ActionResponse(success=True, data={"auth_provider": provider})
            else:
                return ActionResponse(success=False, message=f"Auth provider not found: {name}")

        except Exception as e:
            log.error("GetAuthProviderAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to get auth provider: {e}")

    def find_by_name(self, name: str) -> Optional[dict]:
        """Find auth provider by name."""
        try:
            result = self.gateway.list_auth_providers()
            providers = result.get("authProviders", [])

            for provider in providers:
                if provider.get("name") == name:
                    return provider

            return None
        except Exception as e:
            log.error("GetAuthProviderAction", f"Error finding auth provider: {e}")
            return None

    @classmethod
    def exists(cls, gateway, name: str) -> bool:
        """Check if auth provider exists."""
        action = cls(gateway=gateway)
        return action.find_by_name(name) is not None
