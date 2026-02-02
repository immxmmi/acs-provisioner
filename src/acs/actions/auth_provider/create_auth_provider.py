"""Create Auth Provider action."""

from ..base_action import BaseAction
from .get_auth_provider import GetAuthProviderAction
from model.action_response import ActionResponse
from acs.model.auth_provider_model import AuthProvider
from utils.logger import Logger as log


class CreateAuthProviderAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreateAuthProviderAction", "Starting auth provider creation flow")
            provider = AuthProvider(**data)
            log.debug("CreateAuthProviderAction", f"Resolved model: {provider.model_dump()}")

            # Check if already exists
            log.info("CreateAuthProviderAction", f"Checking existence: {provider.name}")
            existing = GetAuthProviderAction(gateway=self.gateway).find_by_name(provider.name)

            if existing:
                log.info("CreateAuthProviderAction", f"Auth provider already exists, updating: {provider.name}")
                merged = {**existing, **data}
                provider = AuthProvider(**merged)
                payload = provider.to_api_payload()
                result = self.gateway.update_auth_provider(existing["id"], payload)
                log.info("CreateAuthProviderAction", "Auth provider updated successfully")
                return ActionResponse(success=True, data={"auth_provider": provider.name, "id": existing["id"], "result": result})

            # Create new auth provider
            payload = provider.to_api_payload()
            result = self.gateway.create_auth_provider(payload)
            log.info("CreateAuthProviderAction", "Auth provider created successfully")

            return ActionResponse(
                success=True,
                data={"auth_provider": provider.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreateAuthProviderAction", f"Exception occurred: {e}")
            return ActionResponse(
                success=False,
                message=f"Failed to create auth provider: {e}"
            )
