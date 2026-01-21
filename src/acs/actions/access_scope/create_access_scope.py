"""Create Access Scope action."""

from ..base_action import BaseAction
from .get_access_scope import GetAccessScopeAction
from model.action_response import ActionResponse
from acs.model.access_scope_model import AccessScope
from utils.logger import Logger as log


class CreateAccessScopeAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreateAccessScopeAction", "Starting access scope creation flow")
            scope = AccessScope(**data)
            log.debug("CreateAccessScopeAction", f"Resolved model: {scope.model_dump()}")

            # Check if already exists
            log.info("CreateAccessScopeAction", f"Checking existence: {scope.name}")
            existing = GetAccessScopeAction(gateway=self.gateway).find_by_name(scope.name)

            if existing:
                log.info("CreateAccessScopeAction", f"Access scope already exists: {scope.name}")
                return ActionResponse(success=True, data={"access_scope": scope.name, "id": existing.get("id")})

            # Create new access scope
            payload = scope.to_api_payload()
            result = self.gateway.create_access_scope(payload)
            log.info("CreateAccessScopeAction", "Access scope created successfully")

            return ActionResponse(
                success=True,
                data={"access_scope": scope.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreateAccessScopeAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create access scope: {e}")
