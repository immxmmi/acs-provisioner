"""List Policies action."""

from ..base_action import BaseAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class ListPoliciesAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            log.info("ListPoliciesAction", "Listing all policies")
            result = self.gateway.list_policies()
            policies = result.get("policies", [])

            log.info("ListPoliciesAction", f"Found {len(policies)} policies")
            return ActionResponse(
                success=True,
                data={"policies": policies, "count": len(policies)}
            )

        except Exception as e:
            log.error("ListPoliciesAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to list policies: {e}")
