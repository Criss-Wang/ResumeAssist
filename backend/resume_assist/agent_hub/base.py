from resume_assist.engines.factories import load_engine
from resume_assist.utilities.prompt_utils import load_prompt
from resume_assist.utilities.config_utils import load_agent_config
from resume_assist.engines.base_engine import BaseEngine
from resume_assist.app.config import PromptModel


"""
each new agent should have various tasks to consider
agent name from `self.get_agent_name` aligns with the agent field in agents_config.yaml
"""


class Agent:
    def __init__(
        self, task_name: str, use_prompt: bool = True, prompt_version: int = 1
    ):
        self.task_name = task_name

        # load basic agent configurations
        self.config = load_agent_config(self.get_agent_name())

        # load specific engines
        self.engine = self._load_engine()

        # load prompt if necessary
        if use_prompt:
            self.prompt = self._load_prompt(prompt_version)
        else:
            self.prompt = None

    def _load_engine(self) -> BaseEngine:
        engine_config = self.config.engine_config
        engine_class = load_engine(engine_config.engine_type)
        return engine_class(engine_config.model_params, engine_config.model_name)

    def _load_prompt(self, version: int) -> PromptModel:
        engine_config = self.config.engine_config

        section_name = self.task_name
        agent_name = self.get_agent_name()
        engine = engine_config.engine_type
        model = engine_config.model_name
        return load_prompt(section_name, agent_name, version, engine, model)

    def get_agent_name():
        raise NotImplementedError
