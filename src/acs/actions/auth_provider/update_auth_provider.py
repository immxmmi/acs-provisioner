"""Update Auth Provider action."""

from ..base_action import BaseAction
from .get_auth_provider import GetAuthProviderAction
from model.action_response import ActionResponse
from acs.model.auth_provider_model import AuthProvider
from utils.logger import Logger as log


class UpdateAuthProviderAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            log.info("UpdateAuthProviderAction", f"Updating auth provider: {data['name']}")

            # Find existing provider
            existing = GetAuthProviderAction(gateway=self.gateway).find_by_name(data["name"])

            if not existing:
                return ActionResponse(
                    success=False,
                    message=f"Auth provider not found: {data['name']}"
                )

            # Merge existing with updates
            provider_data = {**existing, **data}
            provider = AuthProvider(**provider_data)
            payload = provider.to_api_payload()

            result = self.gateway.update_auth_provider(existing["id"], payload)
            log.info("UpdateAuthProviderAction", "Auth provider updated successfully")

            return ActionResponse(
                success=True,
                data={"auth_provider": provider.name, "id": existing["id"], "result": result}
            )

        except Exception as e:
            log.error("UpdateAuthProviderAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to update auth provider: {e}")
