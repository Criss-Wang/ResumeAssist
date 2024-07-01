from abc import ABC, abstractmethod
from typing import Dict, List


class BaseEngine(ABC):
    def __init__(self, model_params: Dict, model_name: str):
        self.model_name = model_name
        self.model = self.init_model(model_params, model_name)

    @abstractmethod
    def init_model(self, model_params: Dict, model_name: str):
        pass

    def get_model(self):
        return self.model_name

    def get_engine_str(self):
        pass

    def run_instruction(self, messages: List):
        pass
