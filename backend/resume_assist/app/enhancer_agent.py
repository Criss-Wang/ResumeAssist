import logging
from typing import Dict

from resume_assist.agent_hub.base import Agent
from resume_assist.functions import example_function

logger = logging.getLogger(__name__)


class EnhancerAgent(Agent):
    def step(self, input_vars: Dict) -> str:
        """
        Note: these messages can contain system messages, user messages and assistant messages
        """
        system_prompt = self.prompt.system.value
        user_prompt = self.prompt.user.value
        messages = [
            ("system", system_prompt.format(**input_vars)),
            ("user", user_prompt.format(**input_vars)),
        ]
        return self.engine.run_instruction(messages)

    def get_agent_name(self):
        return "enhancer"
