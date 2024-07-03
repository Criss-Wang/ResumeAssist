from typing import Callable
from resume_assist.engines.anthropic_engine import AnthropicEngine
from resume_assist.engines.base_engine import BaseEngine
from resume_assist.app.config import EngineType


def load_engine(engine_type: EngineType) -> Callable:
    if engine_type == EngineType.Anthropic:
        return AnthropicEngine
    else:
        raise NotImplementedError
