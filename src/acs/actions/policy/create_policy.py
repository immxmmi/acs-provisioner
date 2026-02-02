"""Create Policy action."""

from ..base_action import BaseAction
from .get_policy import GetPolicyAction
from model.action_response import ActionResponse
from acs.model.policy_model import Policy
from utils.logger import Logger as log


class CreatePolicyAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("CreatePolicyAction", "Starting policy creation flow")
            policy = Policy(**data)
            log.debug("CreatePolicyAction", f"Resolved model: {policy.model_dump()}")

            # Check if already exists
            log.info("CreatePolicyAction", f"Checking existence: {policy.name}")
            existing = GetPolicyAction(gateway=self.gateway).find_by_name(policy.name)

            if existing:
                log.info("CreatePolicyAction", f"Policy already exists, updating: {policy.name}")
                merged = {**existing, **data}
                policy = Policy(**merged)
                payload = policy.to_api_payload()
                result = self.gateway.update_policy(existing["id"], payload)
                log.info("CreatePolicyAction", "Policy updated successfully")
                return ActionResponse(success=True, data={"policy": policy.name, "id": existing["id"], "result": result})

            # Create new policy
            payload = policy.to_api_payload()
            result = self.gateway.create_policy(payload)
            log.info("CreatePolicyAction", "Policy created successfully")

            return ActionResponse(
                success=True,
                data={"policy": policy.name, "id": result.get("id"), "result": result}
            )

        except Exception as e:
            log.error("CreatePolicyAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to create policy: {e}")
