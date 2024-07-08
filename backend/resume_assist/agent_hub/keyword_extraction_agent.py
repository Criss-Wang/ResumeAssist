import logging
from typing import Dict, List

from resume_assist.agent_hub.base import Agent
from resume_assist.utilities.formatting_utils import (
    parse_to_bullet_pts,
)

logger = logging.getLogger(__name__)


class KeywordExtractionAgent(Agent):
    def extract_keywords(self, job_description: str, limit: int = 5) -> List[str]:
        keywords = self.ner_step({"job_description": job_description})
        keywords = self.filter(keywords, limit)
        return keywords

    def ner_step(self, input_vars: Dict) -> List[str]:
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

    def filter(self, keywords: List[str], limit: int) -> List[str]:
        # TODO: use function calling to achieve robust filtering logic
        return keywords[:limit]

    def get_agent_name(self):
        return "keyword_extractor"
