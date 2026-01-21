"""Create Permission Set action."""

from ..base_action import BaseAction
from .get_permission_set import GetPermissionSetAction
from model.action_response import ActionResponse
from acs.model.permission_set_model import PermissionSet
from utils.logger import Logger as log


class CreatePermissionSetAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreatePermissionSetAction", "Starting permission set creation flow")
            perm_set = PermissionSet(**data)
            log.debug("CreatePermissionSetAction", f"Resolved model: {perm_set.model_dump()}")

            # Check if already exists
            log.info("CreatePermissionSetAction", f"Checking existence: {perm_set.name}")
            existing = GetPermissionSetAction(gateway=self.gateway).find_by_name(perm_set.name)

            if existing:
                log.info("CreatePermissionSetAction", f"Permission set already exists: {perm_set.name}")
                return ActionResponse(success=True, data={"permission_set": perm_set.name, "id": existing.get("id")})

            # Create new permission set
            payload = perm_set.to_api_payload()
            result = self.gateway.create_permission_set(payload)
            log.info("CreatePermissionSetAction", "Permission set created successfully")

            return ActionResponse(
                success=True,
                data={"permission_set": perm_set.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreatePermissionSetAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create permission set: {e}")
