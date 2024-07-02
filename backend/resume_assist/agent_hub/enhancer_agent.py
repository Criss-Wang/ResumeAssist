import logging
from typing import Dict

from resume_assist.agent_hub.base import Agent
from resume_assist.functions import example_function
from resume_assist.utilities.formatting_utils import parse_to_bullet_pts

logger = logging.getLogger(__name__)


class EnhancerAgent(Agent):
    def step(self, input_vars: Dict) -> list[str]:
        """
        Note: these messages can contain system messages, user messages and assistant messages
        """
        system_prompt = self.prompt.system.value
        user_prompt = self.prompt.user.value
        messages = [
            ("system", system_prompt.format(**input_vars)),
            ("user", user_prompt.format(**input_vars)),
        ]
        output = self.engine.run_instruction(messages)
        return parse_to_bullet_pts(output)

    def get_agent_name(self):
        return "enhancer"
