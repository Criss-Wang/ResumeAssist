import logging
from typing import List, Tuple

from resume_assist.agent.agent import Agent
from resume_assist.app.config import AppConfig
from resume_assist.functions import example_function

logger = logging.getLogger(__name__)


class EnhancerAgent(Agent):
    def __init__(self, name: str = None, init_message: str = None, engine: str = None):
        super().__init__(name, init_message, engine)

    def run(self):
        raise NotImplementedError
