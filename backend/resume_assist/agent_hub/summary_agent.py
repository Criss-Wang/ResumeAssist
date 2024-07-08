import logging
from typing import Dict, List

from resume_assist.agent_hub.base import Agent
from resume_assist.utilities.formatting_utils import (
    build_skills_str,
    build_work_str,
    build_project_str,
)

logger = logging.getLogger(__name__)


class SummaryAgent(Agent):
    def step(self, input_vars: Dict) -> List[str]:
        """
        Note: these messages can contain system messages, user messages and assistant messages
        """
        system_prompt = self.prompt.system.value
        user_prompt = self.prompt.user.value
        if self.task_name == "self-intro":
            input_vars = self.update_self_intro_inputs(input_vars)

        messages = [
            ("system", system_prompt.format(**input_vars)),
            ("user", user_prompt.format(**input_vars)),
        ]
        output = self.engine.run_instruction(messages)
        return output

    def update_self_intro_inputs(self, input_vars: Dict):
        assert "job_description" in input_vars
        assert "skills" in input_vars
        assert "work_experiences" in input_vars
        assert "project_experiences" in input_vars

        input_vars["job_description"] += "\n\n"
        input_vars["skills"] = build_skills_str(input_vars["skills"]) + "\n\n"
        input_vars["work_experiences"] = (
            build_work_str(input_vars["work_experiences"]) + "\n\n"
        )
        input_vars["project_experiences"] = (
            build_project_str(input_vars["project_experiences"]) + "\n\n"
        )
        return input_vars

    def get_agent_name(self):
        return "summary"
