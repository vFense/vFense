import logging
import logging.config
from vFense import VFENSE_LOGGING_CONFIG
from vFense.errorz._constants import ApiResultKeys
from vFense.core.operations._constants import AgentOperations, vFensePlugins
from vFense.core.operations.store_agent_operation import StoreAgentOperation

logging.config.fileConfig(VFENSE_LOGGING_CONFIG)
logger = logging.getLogger('rvapi')

class StoreAgentOperations(StoreAgentOperation):
    def reboot(self, agentids=None, tag_id=None):
        results = (
            self.generic_operation(
                AgentOperations.REBOOT,
                vFensePlugins.CORE_PLUGIN,
                agentids, tag_id
            )
        )

        return(results)

    def shutdown(self, agentids=None, tag_id=None):
        results = (
            self.generic_operation(
                AgentOperations.SHUTDOWN,
                vFensePlugins.CORE_PLUGIN,
                agentids, tag_id
            )
        )

        return(results)

    def new_token(self, token, agentids=None, tag_id=None):
        results = (
            self.generic_operation(
                AgentOperations.NEW_TOKEN,
                vFensePlugins.CORE_PLUGIN,
                agentids, tag_id, ApiResultKeys.NEW_TOKEN_ID,
                token
            )
        )

        return(results)
