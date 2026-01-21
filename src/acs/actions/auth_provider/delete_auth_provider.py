"""Delete Auth Provider action."""

from ..base_action import BaseAction
from .get_auth_provider import GetAuthProviderAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeleteAuthProviderAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeleteAuthProviderAction", f"Deleting auth provider: {name}")

            # Find by name to get ID
            provider = GetAuthProviderAction(gateway=self.gateway).find_by_name(name)

            if not provider:
                log.info("DeleteAuthProviderAction", f"Auth provider not found: {name}")
                return ActionResponse(success=True, data={"message": f"Auth provider '{name}' does not exist"})

            provider_id = provider.get("id")
            self.gateway.delete_auth_provider(provider_id)
            log.info("DeleteAuthProviderAction", f"Auth provider deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": provider_id})

        except Exception as e:
            log.error("DeleteAuthProviderAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete auth provider: {e}")
