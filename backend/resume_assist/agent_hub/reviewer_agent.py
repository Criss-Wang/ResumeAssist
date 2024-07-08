import logging
from typing import Dict, List, Tuple

from resume_assist.agent_hub.base import Agent
from resume_assist.utilities.formatting_utils import parse_grading_details

logger = logging.getLogger(__name__)


class ReviewerAgent(Agent):
    def review(
        self,
        original_content: List[str],
        improved_content: List[str],
        job_description: str,
    ) -> Tuple:
        content_grade, reviewer_remark = self.grade(
            {
                "original_content": original_content,
                "improved_content": improved_content,
                "job_description": job_description,
            }
        )
        return content_grade, reviewer_remark

    def grade(self, input_vars: Dict) -> List[str]:
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
        return parse_grading_details(output)

    def get_agent_name(self):
        return "reviewer"
