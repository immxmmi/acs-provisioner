"""Delete Policy action."""

from ..base_action import BaseAction
from .get_policy import GetPolicyAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class DeletePolicyAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("DeletePolicyAction", f"Deleting policy: {name}")

            # Find by name to get ID
            policy = GetPolicyAction(gateway=self.gateway).find_by_name(name)

            if not policy:
                log.info("DeletePolicyAction", f"Policy not found: {name}")
                return ActionResponse(success=True, data={"message": f"Policy '{name}' does not exist"})

            policy_id = policy.get("id")
            self.gateway.delete_policy(policy_id)
            log.info("DeletePolicyAction", f"Policy deleted: {name}")

            return ActionResponse(success=True, data={"deleted": name, "id": policy_id})

        except Exception as e:
            log.error("DeletePolicyAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to delete policy: {e}")
