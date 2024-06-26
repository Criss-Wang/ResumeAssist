from abc import ABC, abstractmethod
from typing import Dict, List


class BaseEngine(ABC):
    def __init__(self, model_params: Dict, model_name: str = "claude-3-opus-20240229"):
        self.model = self.init_model(model_name, model_params)

    @abstractmethod
    def init_model(self, model_params: Dict, model_name: str):
        pass

    def run_instruction(self, messages: List):
        pass
