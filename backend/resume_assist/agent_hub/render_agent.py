import logging
from typing import Dict, List

from resume_assist.agent_hub.base import Agent
from resume_assist.utilities.formatting_utils import (
    parse_to_bullet_pts,
    parse_skill_pts,
)
from resume_assist.functions.cv_rendering import build_cv, build_design, render_pdf

logger = logging.getLogger(__name__)


class RenderAgent(Agent):
    def step(self, input_vars: Dict) -> List[str]:
        try:
            self.run_render(input_vars)
            return True
        except Exception as e:
            print(e)
            return False

    #     system_prompt = self.prompt.system.value
    #     user_prompt = self.prompt.user.value
    #     messages = [
    #         ("system", system_prompt.format(**input_vars)),
    #         ("user", user_prompt.format(**input_vars)),
    #     ]
    #     output = self.engine.run_instruction(messages)
    #     if "skill" in self.task_name:
    #         return parse_skill_pts(output)
    #     return parse_to_bullet_pts(output)

    def run_render(self, cv_info, resume_name: str = "Resume") -> None:
        personal = cv_info["personal"]
        education = cv_info["education"]
        work = cv_info["work"]
        skills = cv_info["skills"]
        projects = cv_info["projects"]
        publications = cv_info["publications"]
        summary = cv_info["summary"]
        cv = build_cv(
            personal, education, work, skills, projects, publications, summary
        )
        design = build_design()
        render_pdf(cv, design, resume_name)

    def get_agent_name(self):
        return "renderer"
