"""Enable Policy action."""

from ..base_action import BaseAction
from .get_policy import GetPolicyAction
from model.action_response import ActionResponse
from utils.logger import Logger as log


class EnablePolicyAction(BaseAction):

    def execute(self, data: dict) -> ActionResponse:
        try:
            self.validate_required(data, "name")
            name = data["name"]

            log.info("EnablePolicyAction", f"Enabling policy: {name}")

            # Find by name to get ID
            policy = GetPolicyAction(gateway=self.gateway).find_by_name(name)

            if not policy:
                return ActionResponse(success=False, message=f"Policy not found: {name}")

            policy_id = policy.get("id")
            self.gateway.enable_policy(policy_id)
            log.info("EnablePolicyAction", f"Policy enabled: {name}")

            return ActionResponse(success=True, data={"enabled": name, "id": policy_id})

        except Exception as e:
            log.error("EnablePolicyAction", f"Exception occurred: {e}")
            return ActionResponse(success=False, message=f"Failed to enable policy: {e}")
